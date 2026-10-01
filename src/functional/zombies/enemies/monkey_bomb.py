""" Monkey Bomb (zombies-only tactical, hotbar.6).

Thrown through the grenade framework (grenade_type "monkey_bomb", 9 s fuse, frag blast); this module only owns the zombie attraction.
Every half-second the monkey redirects nearby zombies through the escort taxi: escorted ones by flagging their trader, the rest with a new escort.
On arrival a zombie holds, frozen: the monkey has no aggro of its own, so a released zombie would walk straight back to the player.
Everything reverts once the monkey is gone.

Dogs are excluded: the escort freezes its passenger with NoAI, and any NBT write on a wolf resets its max health to 8 (see escort).
"""
# Imports
from stewbeet import Mem, write_versioned_function

from .escort.shared import MONKEY_RELEASE

# Constants
MONKEY_ATTRACT_RADIUS: int = 40
""" How far a thrown monkey pulls zombies; matches the enemies' 40-block follow_range. """

MONKEY_REGRAB_FLOOR: int = MONKEY_RELEASE + 2
""" Skips anything already at the monkey, which would otherwise get a taxi for a 0-block walk. """

# Functions
def generate_monkey_bomb() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Run from grenade/init as the thrown grenade item_display, at the throw point.
	write_versioned_function("zombies/monkey/on_throw", f"""
# Read by the attraction hook (grenade/tick) and by cleanup.
tag @s add {ns}.monkey_bomb

# TODO: placeholder until the real toy-jingle .ogg exists.
playsound minecraft:block.note_block.chime ambient @a[distance=..24] ~ ~ ~ 0.8 1.6
""")

	# Run from grenade/tick while a monkey is live.
	write_versioned_function("zombies/monkey/tick", f"""
# Outside a zombies game the monkey is a long-fuse frag.
execute unless data storage {ns}:zombies game{{state:"active"}} run return 0

scoreboard players operation #monkey_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #monkey_phase {ns}.data %= #20 {ns}.data

# Twice a second, nearby zombies are sent to the monkey through the escort taxi.
execute if score #monkey_phase {ns}.data matches 0 run function {ns}:v{version}/zombies/monkey/attract
execute if score #monkey_phase {ns}.data matches 10 run function {ns}:v{version}/zombies/monkey/attract

# Once a second (TODO: real monkey-music .ogg).
execute if score #monkey_phase {ns}.data matches 0 run function {ns}:v{version}/zombies/monkey/pulse
""")

	# Not capped by MAX_ESCORTS: a monkey lives about 9 s and the whole horde should come to it.
	pull_candidates: str = (
		f"@e[tag={ns}.zombie_round,tag=!{ns}.zb_dog,tag=!{ns}.zb_rising,tag=!{ns}.zb_escorted,"
		f"tag=!{ns}.zb_escort_failed,distance={MONKEY_REGRAB_FLOOR}..{MONKEY_ATTRACT_RADIUS}]"
	)
	write_versioned_function("zombies/monkey/attract", f"""
# Zombies already escorted (stuck rescue, PaP lure) are redirected by flagging their trader.
execute as @e[tag={ns}.zombie_round,tag={ns}.zb_escorted,distance=..{MONKEY_ATTRACT_RADIUS}] at @s run function {ns}:v{version}/zombies/escort/redirect_to_monkey

# Every other zombie gets a monkey escort. Not dogs (the escort cannot freeze a wolf); zombies already at the monkey are skipped.
execute as {pull_candidates} at @s run function {ns}:v{version}/zombies/monkey/pull_one
""")

	# Run as the zombie, at it.
	write_versioned_function("zombies/monkey/pull_one", f"""
scoreboard players set #zb_escort_mode {ns}.data 1
function {ns}:v{version}/zombies/escort/start
""")

	# Run as the monkey grenade, at it: no damage, the taxi does the pulling.
	write_versioned_function("zombies/monkey/pulse", f"""
# Chime pitches cycle each pulse, like a little tune (TODO: real monkey-music .ogg).
scoreboard players operation #monkey_note {ns}.data = #total_tick {ns}.data
scoreboard players operation #monkey_note {ns}.data /= #20 {ns}.data
scoreboard players operation #monkey_note {ns}.data %= #4 {ns}.data
execute if score #monkey_note {ns}.data matches 0 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 0.7
execute if score #monkey_note {ns}.data matches 1 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 0.9
execute if score #monkey_note {ns}.data matches 2 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 1.1
execute if score #monkey_note {ns}.data matches 3 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 1.4
particle minecraft:note ~ ~0.5 ~ 0.3 0.3 0.3 1 3 force @a[distance=..32]
""")

