""" Bossbar upkeep for the timed power-ups and the game hooks that drive it. """
# Imports
from stewbeet import Mem, write_versioned_function

from .types import TIMED_POWERUPS, pu_snd


# Functions
def write_powerup_bossbars() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Bossbar update functions — generated from TIMED_POWERUPS, one per entry
	for pu_id, v in TIMED_POWERUPS.items():
		scoreboard: str   = v.scoreboard
		bossbar_id: str   = v.bossbar_id
		# Play the end sound once when the effect transitions from active to expired
		end_sound_line: str = ""
		if v.end_sound:
			end_sound: str = pu_snd(ns, v.end_sound, at_s=True)
			end_sound_line = f"execute if score #pu_prev_{pu_id} {ns}.data matches 1.. if score #pu_max_duration {ns}.data matches ..0 {end_sound}\n"
		write_versioned_function(f"zombies/powerups/update_{pu_id}_bb", f"""
# Find max remaining duration across all players with active {pu_id}
scoreboard players set #pu_max_duration {ns}.data 0
scoreboard players operation #pu_max_duration {ns}.data > @a[scores={{{ns}.special.{scoreboard}=1..}}] {ns}.special.{scoreboard}

# Steady-off fast path: inactive now AND last tick -> no bossbar command at all
# (the bossbar remove used to run every single tick while the powerup was inactive)
execute if score #pu_max_duration {ns}.data matches ..0 if score #pu_prev_{pu_id} {ns}.data matches ..0 run return 0

# If max duration just hit 0, remove bossbar (once); otherwise update value
execute if score #pu_max_duration {ns}.data matches ..0 run bossbar remove {ns}:{bossbar_id}
execute if score #pu_max_duration {ns}.data matches 1.. store result bossbar {ns}:{bossbar_id} value run scoreboard players get #pu_max_duration {ns}.data
{end_sound_line}scoreboard players operation #pu_prev_{pu_id} {ns}.data = #pu_max_duration {ns}.data
""")

	# Hooks into existing systems

	## Insta-kill melee modifier transitions (tag-gated from game_tick above)
	write_versioned_function("zombies/powerups/insta_kill_melee_on", f"""
# remove-then-add keeps this idempotent even if a stale modifier survived a game crash
attribute @s minecraft:attack_damage modifier remove {ns}:insta_kill
attribute @s minecraft:attack_damage modifier add {ns}:insta_kill 100000 add_value
tag @s add {ns}.ik_melee
""")
	write_versioned_function("zombies/powerups/insta_kill_melee_off", f"""
attribute @s minecraft:attack_damage modifier remove {ns}:insta_kill
tag @s remove {ns}.ik_melee
""")

	# Bossbar update calls for game_tick, generated from TIMED_POWERUPS
	bb_update_calls: str = "\n".join(
		f"function {ns}:v{version}/zombies/powerups/update_{pu_id}_bb"
		for pu_id in TIMED_POWERUPS
	)

	# Scoreboard decrement calls for game_tick, generated from TIMED_POWERUPS
	decrement_calls: str = "\n".join(
		f"execute as @a[scores={{{ns}.special.{v.scoreboard}=1..}}] run scoreboard players operation @s {ns}.special.{v.scoreboard} -= #tick_delta {ns}.data"
		for k, v in TIMED_POWERUPS.items()
		if k not in ("insta_kill", "unlimited_ammo") # They are already handled globally (not zombies)
	)

	write_versioned_function("zombies/game_tick", f"""
# Power-up entities exist only after a drop. #pu_active (maintained on spawn/expire/pickup) gates the
# two per-tick scans below so an empty board costs nothing. Resync once every 40 ticks as a safety net
# (the count is already exact since pu_item is Invulnerable and only dies through tracked paths).
execute store result score #pu_active_phase {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #pu_active_phase {ns}.data %= #40 {ns}.data
execute if score #pu_active_phase {ns}.data matches 0 store result score #pu_active {ns}.data if entity @e[type=minecraft:item,tag={ns}.pu_item]

# Power-up entity tick (lifetime countdown, blink, pickup detection)
execute if score #pu_active {ns}.data matches 1.. as @e[type=minecraft:item,tag={ns}.pu_item] at @s run function {ns}:v{version}/zombies/powerups/entity_tick

# Orphan cleanup: a text_display whose item entity was destroyed (burned/exploded) would never
# be removed by expire/pickup — kill any pu_text that no longer has a pu_item beneath it.
execute if score #pu_active {ns}.data matches 1.. as @e[type=minecraft:text_display,tag={ns}.pu_text] at @s unless entity @e[type=minecraft:item,tag={ns}.pu_item,distance=..4] run kill @s

# Insta Kill also works with the knife: give active players a huge melee attack damage so a single
# melee hit one-shots zombies (guns already insta-kill via the raycast path). The {ns}.ik_melee tag
# tracks who currently carries the modifier, so the attribute commands only run on state
# transitions (they used to run for EVERY player EVERY tick, mostly as guaranteed failures).
execute as @a[tag=!{ns}.ik_melee,scores={{{ns}.special.instant_kill=1..}}] run function {ns}:v{version}/zombies/powerups/insta_kill_melee_on
execute as @a[tag={ns}.ik_melee,scores={{{ns}.special.instant_kill=..0}}] run function {ns}:v{version}/zombies/powerups/insta_kill_melee_off

# Blink state: toggles between 0 and 1 every 4 ticks (~0.2s half-cycle, matching BO2's 0.4s full cycle)
scoreboard players add #zb_blink_counter {ns}.data 1
execute if score #zb_blink_counter {ns}.data matches 4.. run scoreboard players set #zb_blink_counter {ns}.data 0
execute if score #zb_blink_counter {ns}.data matches 0 run scoreboard players add #zb_blink_state {ns}.data 1
execute if score #zb_blink_state {ns}.data matches 2.. run scoreboard players set #zb_blink_state {ns}.data 0

# Decrement duration scoreboards
{decrement_calls}

# Update bossbars
{bb_update_calls}

# Fire Sale: global timer countdown + price restore on expiry
execute if score #zb_fire_sale_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/powerups/fire_sale_tick

# Bonfire Sale: global timer countdown
execute if score #zb_bonfire_sale_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/powerups/bonfire_sale_tick
""")

	# stop cleanup resets, generated from TIMED_POWERUPS
	stop_scoreboard_resets: str = "\n".join(
		f"scoreboard players set @a {ns}.special.{v.scoreboard} 0"
		for v in TIMED_POWERUPS.values()
	)
	stop_bossbar_removes: str = "\n".join(
		f"bossbar remove {ns}:{v.bossbar_id}"
		for v in TIMED_POWERUPS.values()
	)

	write_versioned_function("zombies/stop", f"""
# Power-up cleanup
kill @e[type=minecraft:item,tag={ns}.pu_item]
kill @e[type=minecraft:text_display,tag={ns}.pu_text]
scoreboard players set #pu_active {ns}.data 0
scoreboard players set #zb_drops_this_round {ns}.data 0
scoreboard players set #zb_cycle_done {ns}.data 0
scoreboard players set #zb_cycle_len {ns}.data 0
{stop_scoreboard_resets}
data modify storage {ns}:data _pu_queue set value []

# Fire Sale cleanup (reset the global timer + remove its bossbar + stop the song)
scoreboard players set #zb_fire_sale_timer {ns}.data 0
scoreboard players set #mb_fs_cleanup_pending {ns}.data 0
bossbar remove {ns}:pu_fire_sale
stopsound @a ambient {ns}:zombies/powerups/fire_sale_song
tag @e remove {ns}.mb_fs_active
tag @e remove {ns}.mb_orig_active
kill @e[tag={ns}.mb_temp]

# Bonfire Sale cleanup (reset the global timer + remove its bossbar)
scoreboard players set #zb_bonfire_sale_timer {ns}.data 0
bossbar remove {ns}:pu_bonfire_sale

# Remove all duration-based bossbars
{stop_bossbar_removes}
""")

	write_versioned_function("zombies/start_round", f"""
# Reset per-round power-up drop tracking
scoreboard players set #zb_drops_this_round {ns}.data 0
scoreboard players set #zb_cycle_done {ns}.data 0

# Start a fresh shuffle bag for the round; its size = one full drop cycle's worth of drops
function {ns}:v{version}/zombies/powerups/queue_refill
execute store result score #zb_cycle_len {ns}.data run data get storage {ns}:data _pu_queue
""")

	write_versioned_function("zombies/check_kill_points", f"""
# Double points bonus: award the same kill points again if active
execute if score @s {ns}.special.double_points matches 1.. run scoreboard players operation @s {ns}.zb.points += #total_kill_points {ns}.data
""")

	write_versioned_function("zombies/on_hit_signal", f"""
# Double points bonus for bullet hit points
execute if score @n[tag={ns}.ticking] {ns}.special.double_points matches 1.. run scoreboard players operation @n[tag={ns}.ticking] {ns}.zb.points += #zb_points_hit {ns}.config
""")

