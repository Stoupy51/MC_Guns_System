
# Monkey Bomb (zombies-exclusive tactical, hotbar.6)
# Thrown via the generic grenade framework (grenade_type "monkey_bomb", 9s fuse, frag-style blast —
# see weapon/grenade.py init/tick/detonate hooks). This module owns the zombie attraction:
#
# A tiny invulnerable NoAI iron golem ("taunt") follows the thrown monkey. Every second, every
# round enemy within follow range is dealt 0.01 damage BY the taunt: LastHurtByMob feeds the
# HurtByTarget goal (priority 1, above player targeting) so zombies drop their player target and
# path to the monkey instead. Wolves work the same way (being hurt writes their angry_at, which the
# dog retarget loop in round.py explicitly respects). An iron golem is used rather than a villager
# because it has no right-click trade UI; natural zombie targeting of golems is a bonus, the damage
# pulse is the real mechanism. The taunt is on no team, so horde-team enemies can target it.
from stewbeet import Mem, write_load_file, write_versioned_function


def generate_monkey_bomb() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Pairing objective: each monkey grenade and its taunt share an id (several can fly at once)
	write_load_file(f"""
# Monkey bomb grenade <-> attraction taunt pairing
scoreboard objectives add {ns}.monkey_id dummy
""")

	## Called from grenade/init (@s = the freshly thrown grenade item_display, at the throw point)
	write_versioned_function("zombies/monkey/on_throw", f"""
# Tag drives the per-tick attraction hook and lets cleanup find monkey grenades
tag @s add {ns}.monkey_bomb

# Wind-up cue (placeholder: the real toy-jingle .ogg is a HUMAN asset, see zombies README task 8)
playsound minecraft:block.note_block.chime ambient @a[distance=..24] ~ ~ ~ 0.8 1.6

# The taunt only exists inside an active zombies game (elsewhere it's just a long-fuse frag)
execute unless data storage {ns}:zombies game{{state:"active"}} run return 0

# Pair ids, then summon the taunt at the grenade (it follows every tick from zombies/monkey/tick)
scoreboard players add #monkey_id_next {ns}.data 1
scoreboard players operation @s {ns}.monkey_id = #monkey_id_next {ns}.data
summon minecraft:iron_golem ~ ~ ~ {{Tags:["{ns}.monkey_taunt","{ns}.monkey_taunt_new","{ns}.gm_entity"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Attributes:[{{id:"minecraft:scale",base:0.08d}}]}}
scoreboard players operation @n[tag={ns}.monkey_taunt_new] {ns}.monkey_id = @s {ns}.monkey_id
tag @n[tag={ns}.monkey_taunt_new] remove {ns}.monkey_taunt_new
""")

	## Per-tick attraction (called from grenade/tick, @s = monkey grenade, at @s).
	## Cost profile: only runs while a monkey grenade entity exists (the whole grenade loop is
	## gated by #grenade_count), and the aggro pulse itself only fires every 20 ticks.
	write_versioned_function("zombies/monkey/tick", f"""
# Attraction is a zombies-game mechanic only
execute unless data storage {ns}:zombies game{{state:"active"}} run return 0

# Keep the paired taunt on the (bouncing/flying) grenade so enemies path to the right spot
scoreboard players operation #monkey_cur_id {ns}.data = @s {ns}.monkey_id
tag @s add {ns}.monkey_here
execute as @e[tag={ns}.monkey_taunt,distance=..80] if score @s {ns}.monkey_id = #monkey_cur_id {ns}.data run tp @s @n[tag={ns}.monkey_here]
tag @s remove {ns}.monkey_here

# Aggro pulse every second. The fuse score (@s {ns}.data) starts at 180 and this runs before the
# decrement, so skipping 175.. gives pulses at 160, 140, ..., 20 — the first lands ~1s after the
# throw, once the monkey is away from the thrower.
scoreboard players operation #monkey_phase {ns}.data = @s {ns}.data
scoreboard players operation #monkey_phase {ns}.data %= #20 {ns}.data
execute if score #monkey_phase {ns}.data matches 0 unless score @s {ns}.data matches 175.. run function {ns}:v{version}/zombies/monkey/pulse
""")

	## One aggro pulse (@s = monkey grenade, at @s)
	write_versioned_function("zombies/monkey/pulse", f"""
# Mark the paired taunt as the current damage source for this pulse
execute as @e[tag={ns}.monkey_taunt,distance=..8] if score @s {ns}.monkey_id = #monkey_cur_id {ns}.data run tag @s add {ns}.monkey_cur
execute unless entity @e[tag={ns}.monkey_cur,distance=..8] run return 0

# Steal aggro: a 0.01 hit BY the taunt makes each enemy retaliate against it (HurtByTarget beats
# player targeting; also writes wolves' angry_at). 40 blocks matches the enemies' follow_range —
# targets further than that get dropped by vanilla target validation anyway. Rising zombies are
# skipped (NoAI underground); the next pulse catches them once they're up. Re-pulsing every second
# also re-captures enemies that were shot in between (being hurt by a player re-targets them).
execute as @e[tag={ns}.zombie_round,tag=!{ns}.zb_rising,distance=..40] run damage @s 0.01 minecraft:mob_attack by @n[tag={ns}.monkey_cur]
tag @e[tag={ns}.monkey_cur] remove {ns}.monkey_cur

# Toy jingle placeholder: cycle chime pitches each pulse (real monkey-music .ogg is a HUMAN asset)
scoreboard players operation #monkey_note {ns}.data = @s {ns}.data
scoreboard players operation #monkey_note {ns}.data /= #20 {ns}.data
scoreboard players operation #monkey_note {ns}.data %= #4 {ns}.data
execute if score #monkey_note {ns}.data matches 0 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 0.7
execute if score #monkey_note {ns}.data matches 1 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 0.9
execute if score #monkey_note {ns}.data matches 2 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 1.1
execute if score #monkey_note {ns}.data matches 3 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 1.4
particle minecraft:note ~ ~0.5 ~ 0.3 0.3 0.3 1 3 force @a[distance=..32]
""")

	## Detonation (routed from grenade/detonate, @s = monkey grenade, at @s):
	## remove the paired taunt, then reuse the frag explosion (damage attribution included).
	write_versioned_function("zombies/monkey/detonate", f"""
scoreboard players operation #monkey_cur_id {ns}.data = @s {ns}.monkey_id
execute as @e[tag={ns}.monkey_taunt] if score @s {ns}.monkey_id = #monkey_cur_id {ns}.data run kill @s
function {ns}:v{version}/grenade/detonate_frag
""")

	## Hook into stop: remove any leftover taunts (gm_entity cleanup also covers them; explicit for
	## the case where a monkey is still mid-fuse — its grenade outlives the game and detonates as a
	## plain frag, so the taunt must not linger)
	write_versioned_function("zombies/stop", f"""
# Monkey bomb cleanup
kill @e[tag={ns}.monkey_taunt]
scoreboard players set #monkey_id_next {ns}.data 0
""")
