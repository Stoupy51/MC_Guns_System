""" Escort scoreboards, picking a zombie to escort and spawning the trader that leads it. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .shared import ESCORT_TTL, MAX_ESCORTS, PATHFINDING_RANGE


# Functions
def write_escort_start() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
# Ticks left before the teleport-rescue fallback.
scoreboard objectives add {ns}.zb.escort_ttl dummy

# Gates the per-tick escorted-zombie scan.
scoreboard players add #zb_escort_count {ns}.data 0

# One-shot target of the next escort/start, reset there: 0 nearest player (stuck rescue, PaP lure),
# 1 a thrown monkey bomb, 2 the walk-to spot pinned on the zombie (data.walk_to).
scoreboard players add #zb_escort_mode {ns}.data 0

# Zombies and escort traders are allied, so the trader's AvoidEntityGoal(Zombie) never fires (it would flee at sprint speed)
# and zombies never attack it. Created at load, so a mid-game /reload cannot lose it. pushOtherTeams: members do not push
# each other (the zombie overlaps its trader) but still push players and everything else.
team add {ns}.horde
team modify {ns}.horde collisionRule pushOtherTeams
""")

	# Stuck zombies try an escort before the teleport rescue.
	write_versioned_function("zombies/on_stuck_zombie", f"""
# Not for dogs: the escort freezes its passenger with an NBT write, which resets a wolf's MAX_HEALTH base to 8
# (TamableAnimal.setTame), and dogs outrun the trader anyway.
execute unless entity @s[tag={ns}.zb_dog] unless entity @s[tag={ns}.zb_escort_failed] if score #zb_escort_count {ns}.data matches ..{MAX_ESCORTS - 1} run return run function {ns}:v{version}/zombies/escort/start
""", prepend=True)

	# Run as the stuck zombie, at it.
	write_versioned_function("zombies/escort/start", f"""
# The trader walks and drags the frozen zombie. The team join covers zombies summoned before a mid-game /reload added the team.
tag @s add {ns}.zb_escorted
team join {ns}.horde @s
data modify entity @s NoAI set value 1b
scoreboard players set @s {ns}.zb.escort_ttl {ESCORT_TTL}

# While escorted, stuck_x, stuck_z and stuck_ticks hold a block snapshot and a still counter; detach re-initializes them.
execute store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @s {ns}.zb.stuck_ticks 0

# Invisible pathfinding taxi (see the escort module docstring for each NBT choice).
summon minecraft:wandering_trader ~ ~ ~ {{Tags:["{ns}.zb_escort","{ns}.gm_entity","{ns}.zb_escort_new","global.ignore","global.ignore.kill"],Silent:1b,Invulnerable:1b,PersistenceRequired:1b,DespawnDelay:0,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",Offers:{{Recipes:[]}},active_effects:[{{id:"minecraft:invisibility",duration:-1,show_particles:0b}}]}}

team join {ns}.horde @n[tag={ns}.zb_escort_new]

# Trader base speed = zombie speed / 0.35 (WanderToPositionGoal modifier). The base, not the effective value:
# a barricade freeze (-1024) would clamp the taxi to 0, and a just-detached zombie's Speed I would read 20% high.
execute store result storage {ns}:temp _escort.speed double 0.0028571 run attribute @s minecraft:movement_speed base get 1000
execute as @n[tag={ns}.zb_escort_new] run function {ns}:v{version}/zombies/escort/set_trader_speed with storage {ns}:temp _escort

# A big pathfinding budget affords stair detours (PATHFINDING_RANGE); the command triggers the live budget recompute.
execute as @n[tag={ns}.zb_escort_new] run attribute @s minecraft:follow_range base set {PATHFINDING_RANGE}

# Monkey-bomb escorts target the thrown monkey: the flag routes retarget to retarget_monkey.
execute if score #zb_escort_mode {ns}.data matches 1 run tag @n[tag={ns}.zb_escort_new] add {ns}.zb_escort_monkey

# Walk-to spawns: the destination never moves, so the trader carries its own copy.
execute if score #zb_escort_mode {ns}.data matches 2 run tag @n[tag={ns}.zb_escort_new] add {ns}.zb_escort_walk
execute if score #zb_escort_mode {ns}.data matches 2 run data modify entity @n[tag={ns}.zb_escort_new] data.walk_to set from entity @s data.walk_to
scoreboard players set #zb_escort_mode {ns}.data 0

execute as @n[tag={ns}.zb_escort_new] at @s run function {ns}:v{version}/zombies/escort/retarget

tag @n[tag={ns}.zb_escort_new] remove {ns}.zb_escort_new
scoreboard players add #zb_escort_count {ns}.data 1
""")

	write_versioned_function("zombies/escort/set_trader_speed", """
$attribute @s minecraft:movement_speed base set $(speed)
""")

	# Run as a just-risen zombie: escort it to the spot its spawn names. Over the escort cap it spawns normally,
	# with the stuck rescue as the safety net.
	write_versioned_function("zombies/escort/start_to_target", f"""
execute if score #zb_escort_count {ns}.data matches {MAX_ESCORTS}.. run return 0
scoreboard players set #zb_escort_mode {ns}.data 2
function {ns}:v{version}/zombies/escort/start
""")

