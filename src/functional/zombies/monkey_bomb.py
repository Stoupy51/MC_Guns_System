
# Monkey Bomb (zombies-exclusive tactical, hotbar.6)
# Thrown via the generic grenade framework (grenade_type "monkey_bomb", 9s fuse, frag-style blast —
# see weapon/grenade.py init/tick/detonate hooks). This module owns the zombie attraction.
#
# Attraction reuses the escort taxi (escort.py) instead of the old visible iron-golem + fake-damage
# aggro hack: every half-second the thrown monkey (re)directs nearby zombies to itself. Zombies that
# already have an escort (stuck rescue / PaP lure) are redirected by flagging their trader; zombies
# without one get a fresh monkey-targeted escort (uncapped, see the attract pulse below). The
# invisible wandering-trader taxi paths each zombie to the monkey and, on arrival, HOLDS it there
# frozen (escort/monkey_hold) rather than releasing it — the monkey has no aggro of its own, so a
# released zombie immediately walks back to the player. The horde therefore gathers and stays on the
# monkey until the fuse blast clears it. Everything reverts automatically once the monkey is gone —
# escort.py's zombie_tick drops the monkey flag when no monkey_bomb remains.
#
# Dogs are excluded: the escort freezes its passenger with NoAI, and every NBT write on a wolf
# resets its max health to 8 (see escort.py). Dogs are fast and rarely stuck anyway.
from stewbeet import Mem, write_versioned_function

from .escort import MONKEY_RELEASE

# How far a thrown monkey pulls zombies (matches the enemies' 40-block follow_range).
MONKEY_ATTRACT_RADIUS: int = 40
# Don't grab zombies already standing right at the monkey: gathered ones are held by their escort
# (so the tag filters below already skip them), but this also leaves alone anything that wandered in
# on its own — grabbing it would summon a taxi just to walk it zero blocks.
MONKEY_REGRAB_FLOOR: int = MONKEY_RELEASE + 2


def generate_monkey_bomb() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Called from grenade/init (@s = the freshly thrown grenade item_display, at the throw point)
	write_versioned_function("zombies/monkey/on_throw", f"""
# Tag drives the per-tick attraction hook (grenade/tick) and lets cleanup find monkey grenades
tag @s add {ns}.monkey_bomb

# Wind-up cue (placeholder: the real toy-jingle .ogg is a HUMAN asset, see zombies README task 8)
playsound minecraft:block.note_block.chime ambient @a[distance=..24] ~ ~ ~ 0.8 1.6
""")

	## Per-tick hook (called from grenade/tick, @s = monkey grenade, at @s). Cheap: it only runs
	## while a monkey grenade is live, and the attraction/jingle only fire on a cadence.
	write_versioned_function("zombies/monkey/tick", f"""
# Attraction is a zombies-game mechanic only (elsewhere the monkey is just a long-fuse frag)
execute unless data storage {ns}:zombies game{{state:"active"}} run return 0

# Cadence off the global tick counter (main.py increments #total_tick every tick)
scoreboard players operation #monkey_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #monkey_phase {ns}.data %= #20 {ns}.data

# Twice a second: (re)direct nearby zombies to this monkey through the escort taxi
execute if score #monkey_phase {ns}.data matches 0 run function {ns}:v{version}/zombies/monkey/attract
execute if score #monkey_phase {ns}.data matches 10 run function {ns}:v{version}/zombies/monkey/attract

# Once a second: toy-jingle placeholder + note particles (real monkey-music .ogg is a HUMAN asset)
execute if score #monkey_phase {ns}.data matches 0 run function {ns}:v{version}/zombies/monkey/pulse
""")

	## Attraction pulse (@s = monkey grenade, at @s = the monkey's position).
	## Every eligible zombie in radius gets a taxi — no MAX_ESCORTS gate and no limit= on the
	## selector. The cap exists to bound the cost of the STUCK-RESCUE escorts, which run for the
	## whole game; a monkey lives ~9s and its whole point is that the entire horde comes to it, so a
	## half-attracted crowd is worse than the extra traders. Cost while a monkey is out: one
	## wandering trader per zombie in radius, each pathing with PATHFINDING_RANGE (escort.py).
	pull_candidates: str = (
		f"@e[tag={ns}.zombie_round,tag=!{ns}.zb_dog,tag=!{ns}.zb_rising,tag=!{ns}.zb_escorted,"
		f"tag=!{ns}.zb_escort_failed,distance={MONKEY_REGRAB_FLOOR}..{MONKEY_ATTRACT_RADIUS}]"
	)
	write_versioned_function("zombies/monkey/attract", f"""
# Existing escorts near the monkey (stuck rescue / PaP lure): redirect them to it by flagging
# their trader — the "existing escort" case, handled without summoning a second taxi.
execute as @e[tag={ns}.zombie_round,tag={ns}.zb_escorted,distance=..{MONKEY_ATTRACT_RADIUS}] at @s run function {ns}:v{version}/zombies/escort/redirect_to_monkey

# Un-escorted zombies: start a fresh monkey-targeted escort on every one of them. Dogs excluded
# (escort can't freeze a wolf — see the header); the re-grab floor skips whatever is already at the
# monkey.
execute as {pull_candidates} at @s run function {ns}:v{version}/zombies/monkey/pull_one
""")

	## Start one monkey-targeted escort. @s = zombie, at @s
	write_versioned_function("zombies/monkey/pull_one", f"""
scoreboard players set #zb_escort_mode {ns}.data 1
function {ns}:v{version}/zombies/escort/start
""")

	## One jingle pulse (@s = monkey grenade, at @s). No damage — the escort taxi does the pulling.
	write_versioned_function("zombies/monkey/pulse", f"""
# Toy jingle placeholder: cycle chime pitches each pulse so they sound like a little tune
# (real monkey-music .ogg is a HUMAN asset, see zombies README task 8)
scoreboard players operation #monkey_note {ns}.data = #total_tick {ns}.data
scoreboard players operation #monkey_note {ns}.data /= #20 {ns}.data
scoreboard players operation #monkey_note {ns}.data %= #4 {ns}.data
execute if score #monkey_note {ns}.data matches 0 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 0.7
execute if score #monkey_note {ns}.data matches 1 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 0.9
execute if score #monkey_note {ns}.data matches 2 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 1.1
execute if score #monkey_note {ns}.data matches 3 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 1.4
particle minecraft:note ~ ~0.5 ~ 0.3 0.3 0.3 1 3 force @a[distance=..32]
""")

