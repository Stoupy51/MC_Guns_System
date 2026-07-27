""" Monkey Bomb (zombies-exclusive tactical, hotbar.6).

Thrown via the generic grenade framework (grenade_type "monkey_bomb", 9s fuse, frag blast); this
module owns only the zombie attraction. Every half-second the monkey redirects nearby zombies
through the escort taxi (escort.py): already-escorted ones by flagging their trader, the rest by
starting a fresh monkey-targeted escort. On arrival a zombie HOLDS frozen rather than releasing,
since the monkey has no aggro of its own and a released zombie would walk straight back to the
player. Everything reverts once the monkey is gone.

Dogs are excluded: the escort freezes its passenger with NoAI, and every NBT write on a wolf resets
its max health to 8 (see escort.py). Dogs are fast and rarely stuck anyway.
"""
# Imports
from stewbeet import Mem, write_versioned_function

from .escort import MONKEY_RELEASE

# Constants
MONKEY_ATTRACT_RADIUS: int = 40
""" How far a thrown monkey pulls zombies; matches the enemies' 40-block follow_range. """

MONKEY_REGRAB_FLOOR: int = MONKEY_RELEASE + 2
""" Leaves alone anything already at the monkey — grabbing it would summon a taxi to walk 0 blocks. """

# Functions
def generate_monkey_bomb() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Called from grenade/init (@s = the freshly thrown grenade item_display, at the throw point)
	write_versioned_function("zombies/monkey/on_throw", f"""
# Tag drives the per-tick attraction hook (grenade/tick) and lets cleanup find monkey grenades
tag @s add {ns}.monkey_bomb

# Wind-up cue (placeholder: the real toy-jingle .ogg is a HUMAN asset, see zombies README task 8)
playsound minecraft:block.note_block.chime ambient @a[distance=..24] ~ ~ ~ 0.8 1.6
""")

	# Per-tick hook from grenade/tick; only runs while a monkey is live, and pulses on a cadence
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

	# Uncapped on purpose: MAX_ESCORTS bounds the whole-game stuck rescues, but a monkey lives ~9s.
	# Its point is that the entire horde comes to it, so a half-attracted crowd is worse.
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

	# Start one monkey-targeted escort (@s = zombie, at @s)
	write_versioned_function("zombies/monkey/pull_one", f"""
scoreboard players set #zb_escort_mode {ns}.data 1
function {ns}:v{version}/zombies/escort/start
""")

	# One jingle pulse (@s = monkey grenade, at @s); no damage, the taxi does the pulling
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

