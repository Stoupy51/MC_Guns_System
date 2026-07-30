""" Game hooks, the per-round reset and the Carpenter power-up repair. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_barricade_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Hook into game tick — single @e sweep for all barricade displays
	write_versioned_function("zombies/game_tick", f"""
# Barricades: restore frozen speeds from last tick, then dispatch all display ticks
execute as @e[tag={ns}.zombie_round,tag={ns}.barricade_frozen] run function {ns}:v{version}/zombies/barricades/restore_zombie_speed
execute as @e[type=minecraft:block_display,tag={ns}.barricade_display] at @s run function {ns}:v{version}/zombies/barricades/tick

# Refresh barricade brightness every 5s (local light can change: doors, power, placed lights)
scoreboard players add #barricade_bright_timer {ns}.data 1
execute if score #barricade_bright_timer {ns}.data matches 100.. run scoreboard players set #barricade_bright_timer {ns}.data 0
execute if score #barricade_bright_timer {ns}.data matches 0 as @e[type=minecraft:block_display,tag={ns}.barricade_display] at @s run function {ns}:v{version}/zombies/barricades/compute_brightness
""")

	## Hook into preload_complete — setup barricades if map has any
	write_versioned_function("zombies/preload_complete", f"""
# Maps saved before the barriers->barricades rename still carry the old key, and maps.py only appends a
# map "unless" its id already exists, so an existing world keeps its old compound forever. Normalise the
# key here instead of migrating: game.map is a per-game copy (helpers/lifecycle.py), so this never writes
# to the stored map, and everything downstream only has to know about `barricades`.
execute unless data storage {ns}:zombies game.map.barricades if data storage {ns}:zombies game.map.barriers run data modify storage {ns}:zombies game.map.barricades set from storage {ns}:zombies game.map.barriers

# Setup barricades
execute if data storage {ns}:zombies game.map.barricades[0] run function {ns}:v{version}/zombies/barricades/setup
""")

	## Reset repair counter at the start of each round
	write_versioned_function("zombies/on_round_start", f"""
# Reset barricade repair counters for all players
scoreboard players set @a {ns}.zb.barricade_repairs 0
""")

	## Hook into stop — clean up tags on living entities (gm_entity kill handles the entities)
	write_versioned_function("zombies/stop", f"""
# Barricades cleanup
tag @e[tag={ns}.barricade_removing] remove {ns}.barricade_removing
tag @a[tag={ns}.barricade_repairing] remove {ns}.barricade_repairing
scoreboard players reset @a {ns}.zb.barricade_repairs
""")

	## Carpenter: instantly repair every barricade in the broken state
	write_versioned_function("zombies/barricades/repair_all", f"""
execute as @e[type=minecraft:block_display,tag={ns}.barricade_display,scores={{{ns}.zb.barricade.state=1}}] at @s run function {ns}:v{version}/zombies/barricades/instant_repair
""")

	## Instantly repair a single barricade entity (run as the item_display entity, at @s)
	write_versioned_function("zombies/barricades/instant_repair", f"""
# Set barricade to intact state
scoreboard players set @s {ns}.zb.barricade.state 0

# Clear any in-progress remove / repair counters so no stale IDs linger
scoreboard players set @s {ns}.zb.barricade.repairing_id 0
scoreboard players set @s {ns}.zb.barricade.removing_id 0

# Release any zombie or player currently acting on this barricade
tag @e[tag={ns}.barricade_removing,scores={{{ns}.zb.barricade.removing_id=1..}}] remove {ns}.barricade_removing
tag @a[tag={ns}.barricade_repairing] remove {ns}.barricade_repairing

# Re-enable the block (collision/visibility)
data modify entity @s block_state set from entity @s data.block_enabled

# Visual feedback
particle minecraft:happy_villager ~ ~ ~ 0.5 0.5 0.5 0.05 10 normal
playsound minecraft:block.wood.place block @a[distance=..32] ~ ~ ~ 1.0 1.0
""")

