""" Game hooks, the per-round reset and the Carpenter power-up repair. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_barrier_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Hook into game tick — single @e sweep for all barrier displays
	write_versioned_function("zombies/game_tick", f"""
# Barriers: restore frozen speeds from last tick, then dispatch all display ticks
execute as @e[tag={ns}.zombie_round,tag={ns}.barrier_frozen] run function {ns}:v{version}/zombies/barriers/restore_zombie_speed
execute as @e[type=minecraft:block_display,tag={ns}.barrier_display] at @s run function {ns}:v{version}/zombies/barriers/tick

# Refresh barricade brightness every 5s (local light can change: doors, power, placed lights)
scoreboard players add #barrier_bright_timer {ns}.data 1
execute if score #barrier_bright_timer {ns}.data matches 100.. run scoreboard players set #barrier_bright_timer {ns}.data 0
execute if score #barrier_bright_timer {ns}.data matches 0 as @e[type=minecraft:block_display,tag={ns}.barrier_display] at @s run function {ns}:v{version}/zombies/barriers/compute_brightness
""")

	## Hook into preload_complete — setup barriers if map has any
	write_versioned_function("zombies/preload_complete", f"""
# Setup barriers
execute if data storage {ns}:zombies game.map.barriers[0] run function {ns}:v{version}/zombies/barriers/setup
""")

	## Reset repair counter at the start of each round
	write_versioned_function("zombies/on_round_start", f"""
# Reset barrier repair counters for all players
scoreboard players set @a {ns}.zb.barrier_repairs 0
""")

	## Hook into stop — clean up tags on living entities (gm_entity kill handles the entities)
	write_versioned_function("zombies/stop", f"""
# Barriers cleanup
tag @e[tag={ns}.barrier_removing] remove {ns}.barrier_removing
tag @a[tag={ns}.barrier_repairing] remove {ns}.barrier_repairing
scoreboard players reset @a {ns}.zb.barrier_repairs
""")

	## Carpenter: instantly repair every barrier in the broken state
	write_versioned_function("zombies/barriers/repair_all", f"""
execute as @e[type=minecraft:block_display,tag={ns}.barrier_display,scores={{{ns}.zb.barrier.state=1}}] at @s run function {ns}:v{version}/zombies/barriers/instant_repair
""")

	## Instantly repair a single barrier entity (run as the item_display entity, at @s)
	write_versioned_function("zombies/barriers/instant_repair", f"""
# Set barrier to intact state
scoreboard players set @s {ns}.zb.barrier.state 0

# Clear any in-progress remove / repair counters so no stale IDs linger
scoreboard players set @s {ns}.zb.barrier.repairing_id 0
scoreboard players set @s {ns}.zb.barrier.removing_id 0

# Release any zombie or player currently acting on this barrier
tag @e[tag={ns}.barrier_removing,scores={{{ns}.zb.barrier.removing_id=1..}}] remove {ns}.barrier_removing
tag @a[tag={ns}.barrier_repairing] remove {ns}.barrier_repairing

# Re-enable the block (collision/visibility)
data modify entity @s block_state set from entity @s data.block_enabled

# Visual feedback
particle minecraft:happy_villager ~ ~ ~ 0.5 0.5 0.5 0.05 10 normal
playsound minecraft:block.wood.place block @a[distance=..32] ~ ~ ~ 1.0 1.0
""")

