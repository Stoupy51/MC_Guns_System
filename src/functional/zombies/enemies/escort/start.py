""" Escort scoreboards, picking a zombie to escort and spawning the trader that leads it. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .shared import ESCORT_TTL, MAX_ESCORTS, PATHFINDING_RANGE


# Functions
def write_escort_start() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
# Escort TTL per escorted zombie (ticks left before the teleport-rescue fallback)
scoreboard objectives add {ns}.zb.escort_ttl dummy

# Live escort counter (gates the per-tick escorted-zombie scan)
scoreboard players add #zb_escort_count {ns}.data 0

# One-shot target mode for the NEXT escort/start, consumed (reset to 0) inside start:
# 0 = aim at the nearest player (stuck rescue / PaP lure), 1 = aim at a thrown monkey bomb,
# 2 = aim at the spot a walk-to spawn pinned on the zombie (data.walk_to).
scoreboard players add #zb_escort_mode {ns}.data 0

# Horde alliance team: round zombies and escort traders are allied, so the trader's
# AvoidEntityGoal(Zombie) never fires (it flees at SPRINT speed otherwise!) and zombies never
# attack the taxi. Created at load, not game start, so a mid-game /reload can't leave it missing.
# pushOtherTeams = no pushing WITHIN the horde (the zombie overlaps its trader without shoving
# it off its path) while members still push players and everything else.
team add {ns}.horde
team modify {ns}.horde collisionRule pushOtherTeams
""")

	# Route stuck zombies to an escort before the teleport-rescue body in on_stuck_zombie (game.py)
	write_versioned_function("zombies/on_stuck_zombie", f"""
# Prefer a wandering-trader escort over the teleport rescue below (see escort.py).
# Dogs are excluded: the escort freezes its passenger with `data modify entity @s NoAI`, and every
# NBT write on a wolf runs readAdditionalSaveData -> setTame(false,true) -> MAX_HEALTH base reset
# to 8 (TamableAnimal/Wolf). A dog dragged by a taxi arrives at 8 HP, dying to anything it touches.
# They also don't need one — they outrun the trader, so the direct teleport below is strictly better.
execute unless entity @s[tag={ns}.zb_dog] unless entity @s[tag={ns}.zb_escort_failed] if score #zb_escort_count {ns}.data matches ..{MAX_ESCORTS - 1} run return run function {ns}:v{version}/zombies/escort/start
""", prepend=True)

	# Start an escort (@s = stuck zombie, at @s)
	write_versioned_function("zombies/escort/start", f"""
# Freeze the zombie: the trader does the walking from here, the zombie is dragged behind it.
# The team join is normally redundant (round.py joins every zombie at summon) but covers
# zombies summoned before a mid-game /reload introduced the team.
tag @s add {ns}.zb_escorted
team join {ns}.horde @s
data modify entity @s NoAI set value 1b
scoreboard players set @s {ns}.zb.escort_ttl {ESCORT_TTL}

# Watchdog init: stuck_x/z/ticks are repurposed while escorted (block snapshot + still counter);
# detach re-initializes them for the normal stuck detection
execute store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @s {ns}.zb.stuck_ticks 0

# Invisible pathfinding taxi (see escort.py header for every NBT choice)
summon minecraft:wandering_trader ~ ~ ~ {{Tags:["{ns}.zb_escort","{ns}.gm_entity","{ns}.zb_escort_new","global.ignore","global.ignore.kill"],Silent:1b,Invulnerable:1b,PersistenceRequired:1b,DespawnDelay:0,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",Offers:{{Recipes:[]}},active_effects:[{{id:"minecraft:invisibility",duration:-1,show_particles:0b}}]}}

# Allied with the horde so its AvoidEntityGoal(Zombie) never fires and zombies never target it
team join {ns}.horde @n[tag={ns}.zb_escort_new]

# Trader base speed = zombie_speed / 0.35 (WanderToPositionGoal modifier) => same effective speed.
# BASE get, not effective: a barrier-frozen zombie's {ns}:freeze modifier (-1024) would read negative
# and clamp the taxi to 0 speed; a just-detached zombie's Speed I would read 20% high.
execute store result storage {ns}:temp _escort.speed double 0.0028571 run attribute @s minecraft:movement_speed base get 1000
execute as @n[tag={ns}.zb_escort_new] run function {ns}:v{version}/zombies/escort/set_trader_speed with storage {ns}:temp _escort

# Big pathfinding budget so it can afford stair detours instead of camping below the player
# (see PATHFINDING_RANGE in escort.py; the command triggers the live budget recompute)
execute as @n[tag={ns}.zb_escort_new] run attribute @s minecraft:follow_range base set {PATHFINDING_RANGE}

# Monkey-bomb escorts (monkey_bomb.py) target the thrown monkey instead of a player: flag the
# trader so retarget routes to retarget_monkey. #zb_escort_mode is the caller's one-shot signal.
execute if score #zb_escort_mode {ns}.data matches 1 run tag @n[tag={ns}.zb_escort_new] add {ns}.zb_escort_monkey

# Walk-to spawns (start_to_target): the destination never moves, so the trader carries its own copy
# of it and retarget just feeds that straight back in, no lookup per second.
execute if score #zb_escort_mode {ns}.data matches 2 run tag @n[tag={ns}.zb_escort_new] add {ns}.zb_escort_walk
execute if score #zb_escort_mode {ns}.data matches 2 run data modify entity @n[tag={ns}.zb_escort_new] data.walk_to set from entity @s data.walk_to
scoreboard players set #zb_escort_mode {ns}.data 0

# Aim it at its target immediately (nearest player, PaP-room lure, or thrown monkey per the flag)
execute as @n[tag={ns}.zb_escort_new] at @s run function {ns}:v{version}/zombies/escort/retarget

tag @n[tag={ns}.zb_escort_new] remove {ns}.zb_escort_new
scoreboard players add #zb_escort_count {ns}.data 1
""")

	write_versioned_function("zombies/escort/set_trader_speed", """
$attribute @s minecraft:movement_speed base set $(speed)
""")

	# Escort a just-risen zombie to the spot its spawn point named (@s = that zombie, at @s).
	# Over the escort cap it simply doesn't get one: it spawns like any other zombie and the stuck
	# rescue remains the safety net, which is strictly better than starving the rescues themselves.
	write_versioned_function("zombies/escort/start_to_target", f"""
execute if score #zb_escort_count {ns}.data matches {MAX_ESCORTS}.. run return 0
scoreboard players set #zb_escort_mode {ns}.data 2
function {ns}:v{version}/zombies/escort/start
""")

