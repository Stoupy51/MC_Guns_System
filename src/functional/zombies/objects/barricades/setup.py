""" Barricade scoreboards and summoning a block_display per barricade. """
# Imports
from stewbeet import (
	JsonDict,
	Mem,
	Predicate,
	set_json_encoder,
	write_load_file,
	write_versioned_function,
)


# Functions
def write_barricade_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## One exact-match predicate per light level (the StewBeet custom_blocks technique).
	for level in range(1, 16):
		light_pred: JsonDict = {"type": "minecraft:location_check", "predicate": {"light": {"light": level}}}
		Mem.ctx.data[ns].predicates[f"v{version}/light/{level}"] = set_json_encoder(Predicate(light_pred), max_level=-1)

	write_load_file(f"""
scoreboard objectives add {ns}.zb.barricade.id dummy
scoreboard objectives add {ns}.zb.barricade.state dummy
scoreboard objectives add {ns}.zb.barricade.r_timer dummy
scoreboard objectives add {ns}.zb.barricade.rp_timer dummy
scoreboard objectives add {ns}.zb.barricade.radius dummy
scoreboard objectives add {ns}.zb.barricade.removing_id dummy
scoreboard objectives add {ns}.zb.barricade.repairing_id dummy
# Reset each round; only 25 repairs per round pay.
scoreboard objectives add {ns}.zb.barricade_repairs dummy

# #total_tick when each barricade sound frees up, as in vocals: never reset, and an unset score reads as ready.
scoreboard objectives add {ns}.zb.barricade.bang_at dummy
scoreboard objectives add {ns}.zb.barricade.rep_at dummy
""")

	write_versioned_function("zombies/barricades/setup", f"""
scoreboard players set #barricade_counter {ns}.data 0
data modify storage {ns}:temp _barricade_iter set from storage {ns}:zombies game.map.barricades
execute if data storage {ns}:temp _barricade_iter[0] run function {ns}:v{version}/zombies/barricades/setup_iter
""")

	write_versioned_function("zombies/barricades/setup_iter", f"""
scoreboard players add #barricade_counter {ns}.data 1

execute store result score #bx {ns}.data run data get storage {ns}:temp _barricade_iter[0].pos[0]
execute store result score #by {ns}.data run data get storage {ns}:temp _barricade_iter[0].pos[1]
execute store result score #bz {ns}.data run data get storage {ns}:temp _barricade_iter[0].pos[2]
scoreboard players operation #bx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #by {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bz {ns}.data += #gm_base_z {ns}.data

# Float to score x100 to double x0.01.
execute store result score #byaw {ns}.data run data get storage {ns}:temp _barricade_iter[0].rotation[0] 100

execute store result storage {ns}:temp _bplace.x double 1 run scoreboard players get #bx {ns}.data
execute store result storage {ns}:temp _bplace.y double 1 run scoreboard players get #by {ns}.data
execute store result storage {ns}:temp _bplace.z double 1 run scoreboard players get #bz {ns}.data
execute store result storage {ns}:temp _bplace.yaw double 0.01 run scoreboard players get #byaw {ns}.data

function {ns}:v{version}/zombies/barricades/place_at with storage {ns}:temp _bplace

# All zb_object data (block_enabled, block_disabled, radius, ...).
execute as @n[tag={ns}._barricade_new_d] run data modify entity @s data set from storage {ns}:temp _barricade_iter[0]

# Fill the blocks a map leaves out at their default, and upgrade pre-26.3 block states.
execute as @n[tag={ns}._barricade_new_d] run function {ns}:v{version}/maps/light_fields/barricade

execute as @n[tag={ns}._barricade_new_d] run data modify entity @s block_state set from entity @s data.block_enabled

scoreboard players operation @n[tag={ns}._barricade_new_d] {ns}.zb.barricade.id = #barricade_counter {ns}.data
execute store result score @n[tag={ns}._barricade_new_d] {ns}.zb.barricade.radius run data get storage {ns}:temp _barricade_iter[0].radius
scoreboard players set @n[tag={ns}._barricade_new_d] {ns}.zb.barricade.state 0
scoreboard players set @n[tag={ns}._barricade_new_d] {ns}.zb.barricade.r_timer 0
scoreboard players set @n[tag={ns}._barricade_new_d] {ns}.zb.barricade.rp_timer 0

execute as @n[tag={ns}._barricade_new_d] at @s run function {ns}:v{version}/zombies/barricades/compute_brightness

tag @e[tag={ns}._barricade_new_d] remove {ns}._barricade_new_d

data remove storage {ns}:temp _barricade_iter[0]
execute if data storage {ns}:temp _barricade_iter[0] run function {ns}:v{version}/zombies/barricades/setup_iter
""")

	write_versioned_function("zombies/barricades/place_at", f"""
$execute positioned $(x) $(y) $(z) align xyz positioned ~.5 ~.5 ~.5 run summon minecraft:block_display ~ ~ ~ {{Rotation:[$(yaw)f,0f],block_state:"minecraft:air",transformation:{{left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],translation:[-0.5f,-0.5f,-0.5f],right_rotation:[0f,0f,0f,1f]}},Tags:["{ns}.barricade_display","{ns}.gm_entity","{ns}._barricade_new_d"]}}
""")

