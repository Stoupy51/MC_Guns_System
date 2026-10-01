""" Ejected bullet casings: summon, physics and cleanup. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import (
	CASING_BINORMAL,
	CASING_MODEL,
	CASING_NORMAL,
	CASING_OFFSET,
	CASING_TANGENT,
)


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("player/right_click", f"""
function {ns}:v{version}/casing/main
""")

	item_nbt: str = f"""{{Tags:["{ns}.new","{ns}.casing"],Item:{{id:"minecraft:stone",count:1,components:{{"minecraft:item_model":"air"}}}},PickupDelay:32767,Age:5990}}"""

	write_versioned_function("casing/main", f"""
scoreboard players set #is_zoom {ns}.data 0
execute if data storage {ns}:gun all.stats.is_zoom run scoreboard players set #is_zoom {ns}.data 1

scoreboard players set #casing_normal {ns}.data 0
scoreboard players set #casing_tangent {ns}.data 0
scoreboard players set #casing_binormal {ns}.data 0
execute store result score #casing_normal {ns}.data run data get storage {ns}:gun all.stats.{CASING_NORMAL}
execute store result score #casing_tangent {ns}.data run data get storage {ns}:gun all.stats.{CASING_TANGENT}
execute store result score #casing_binormal {ns}.data run data get storage {ns}:gun all.stats.{CASING_BINORMAL}

execute unless data storage {ns}:gun all.stats.{CASING_MODEL} run return fail

# Random variation of the tangent.
scoreboard players set #random_variation {ns}.data 40
execute store result score #random_variation {ns}.data run random value 0..39
scoreboard players remove #random_variation {ns}.data 20
scoreboard players operation #casing_tangent {ns}.data += #random_variation {ns}.data

execute anchored eyes positioned ^ ^ ^ summon marker run function {ns}:v{version}/casing/process_vectors

data modify storage {ns}:temp casing set value {{Item:{{components:{{}}}},Motion:[0.0d,0.0d,0.0d],Pos:[0.0d,0.0d,0.0d]}}
data modify storage {ns}:temp casing.Item.components."minecraft:item_model" set from storage {ns}:gun all.stats.{CASING_MODEL}
execute store result storage {ns}:temp casing.Motion[0] double 0.001 run scoreboard players get #motion_x {ns}.data
execute store result storage {ns}:temp casing.Motion[1] double 0.001 run scoreboard players get #motion_y {ns}.data
execute store result storage {ns}:temp casing.Motion[2] double 0.001 run scoreboard players get #motion_z {ns}.data

execute store result storage {ns}:temp casing.Pos[0] double 0.001 run scoreboard players get #pos_new_x {ns}.data
execute store result storage {ns}:temp casing.Pos[1] double 0.001 run scoreboard players get #pos_new_y {ns}.data
execute store result storage {ns}:temp casing.Pos[2] double 0.001 run scoreboard players get #pos_new_z {ns}.data

summon item ~ ~ ~ {item_nbt}
execute as @n[type=item,tag={ns}.new] run function {ns}:v{version}/casing/update_item
""")

	write_versioned_function("casing/update_item", f"""
data modify entity @s {{}} merge from storage {ns}:temp casing
tag @s remove {ns}.new
""")

	write_versioned_function("casing/process_vectors", f"""
function {ns}:v{version}/casing/calculate_vectors

function {ns}:v{version}/casing/calculate_motion

function {ns}:v{version}/casing/calculate_offset

kill @s
""")

	# Normal, tangent and binormal of the look direction, from marker moves of 1 block along each local axis.
	write_versioned_function("casing/calculate_vectors", f"""

tp @s ~ ~ ~ ~ ~
execute store result score #pos_initial_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #pos_initial_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #pos_initial_z {ns}.data run data get entity @s Pos[2] 1000

## Normal (local Y)

tp @s ^ ^1 ^

execute store result score #normal_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #normal_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #normal_z {ns}.data run data get entity @s Pos[2] 1000
scoreboard players operation #normal_x {ns}.data -= #pos_initial_x {ns}.data
scoreboard players operation #normal_y {ns}.data -= #pos_initial_y {ns}.data
scoreboard players operation #normal_z {ns}.data -= #pos_initial_z {ns}.data

# Scaled into separate scores so the raw normals stay intact.
scoreboard players operation #scaled_normal_x {ns}.data = #normal_x {ns}.data
scoreboard players operation #scaled_normal_x {ns}.data *= #casing_normal {ns}.data
scoreboard players operation #scaled_normal_y {ns}.data = #normal_y {ns}.data
scoreboard players operation #scaled_normal_y {ns}.data *= #casing_normal {ns}.data
scoreboard players operation #scaled_normal_z {ns}.data = #normal_z {ns}.data
scoreboard players operation #scaled_normal_z {ns}.data *= #casing_normal {ns}.data

## Tangent (local Z)

tp @s ^ ^ ^1
execute store result score #tangent_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #tangent_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #tangent_z {ns}.data run data get entity @s Pos[2] 1000
scoreboard players operation #tangent_x {ns}.data -= #pos_initial_x {ns}.data
scoreboard players operation #tangent_y {ns}.data -= #pos_initial_y {ns}.data
scoreboard players operation #tangent_z {ns}.data -= #pos_initial_z {ns}.data

scoreboard players operation #scaled_tangent_x {ns}.data = #tangent_x {ns}.data
scoreboard players operation #scaled_tangent_x {ns}.data *= #casing_tangent {ns}.data
scoreboard players operation #scaled_tangent_y {ns}.data = #tangent_y {ns}.data
scoreboard players operation #scaled_tangent_y {ns}.data *= #casing_tangent {ns}.data
scoreboard players operation #scaled_tangent_z {ns}.data = #tangent_z {ns}.data
scoreboard players operation #scaled_tangent_z {ns}.data *= #casing_tangent {ns}.data

## Binormal (local X)

tp @s ^1 ^ ^
execute store result score #binormal_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #binormal_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #binormal_z {ns}.data run data get entity @s Pos[2] 1000
scoreboard players operation #binormal_x {ns}.data -= #pos_initial_x {ns}.data
scoreboard players operation #binormal_y {ns}.data -= #pos_initial_y {ns}.data
scoreboard players operation #binormal_z {ns}.data -= #pos_initial_z {ns}.data

scoreboard players operation #scaled_binormal_x {ns}.data = #binormal_x {ns}.data
scoreboard players operation #scaled_binormal_x {ns}.data *= #casing_binormal {ns}.data
scoreboard players operation #scaled_binormal_y {ns}.data = #binormal_y {ns}.data
scoreboard players operation #scaled_binormal_y {ns}.data *= #casing_binormal {ns}.data
scoreboard players operation #scaled_binormal_z {ns}.data = #binormal_z {ns}.data
scoreboard players operation #scaled_binormal_z {ns}.data *= #casing_binormal {ns}.data
""")

	write_versioned_function("casing/calculate_motion", f"""
### Motion = scaled normal + tangent + binormal.

scoreboard players operation #motion_x {ns}.data = #scaled_normal_x {ns}.data
scoreboard players operation #motion_y {ns}.data = #scaled_normal_y {ns}.data
scoreboard players operation #motion_z {ns}.data = #scaled_normal_z {ns}.data

scoreboard players operation #motion_x {ns}.data += #scaled_tangent_x {ns}.data
scoreboard players operation #motion_y {ns}.data += #scaled_tangent_y {ns}.data
scoreboard players operation #motion_z {ns}.data += #scaled_tangent_z {ns}.data

scoreboard players operation #motion_x {ns}.data += #scaled_binormal_x {ns}.data
scoreboard players operation #motion_z {ns}.data += #scaled_binormal_z {ns}.data

# The vectors are x1000 integers.
scoreboard players operation #motion_x {ns}.data /= #1000 {ns}.data
scoreboard players operation #motion_y {ns}.data /= #1000 {ns}.data
scoreboard players operation #motion_z {ns}.data /= #1000 {ns}.data
""")

	write_versioned_function("casing/calculate_offset", f"""
### Local casing offsets to world coordinates, through the gun's orientation vectors.

# Local offsets, x1000.
execute if score #is_zoom {ns}.data matches 0 store result score #offset_x {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.normal[0] 1000
execute if score #is_zoom {ns}.data matches 0 store result score #offset_y {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.normal[1] 1000
execute if score #is_zoom {ns}.data matches 0 store result score #offset_z {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.normal[2] 1000
execute if score #is_zoom {ns}.data matches 1 store result score #offset_x {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.zoom[0] 1000
execute if score #is_zoom {ns}.data matches 1 store result score #offset_y {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.zoom[1] 1000
execute if score #is_zoom {ns}.data matches 1 store result score #offset_z {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.zoom[2] 1000

# Each axis is the sum of the offsets projected on binormal, normal and tangent, plus the start position.
scoreboard players operation #off_bx {ns}.data = #binormal_x {ns}.data
scoreboard players operation #off_bx {ns}.data *= #offset_x {ns}.data
scoreboard players operation #off_nx {ns}.data = #normal_x {ns}.data
scoreboard players operation #off_nx {ns}.data *= #offset_y {ns}.data
scoreboard players operation #off_tx {ns}.data = #tangent_x {ns}.data
scoreboard players operation #off_tx {ns}.data *= #offset_z {ns}.data

scoreboard players operation #pos_new_x {ns}.data = #off_bx {ns}.data
scoreboard players operation #pos_new_x {ns}.data += #off_nx {ns}.data
scoreboard players operation #pos_new_x {ns}.data += #off_tx {ns}.data
scoreboard players operation #pos_new_x {ns}.data /= #1000 {ns}.data

scoreboard players operation #pos_new_x {ns}.data += #pos_initial_x {ns}.data

scoreboard players operation #off_by {ns}.data = #binormal_y {ns}.data
scoreboard players operation #off_by {ns}.data *= #offset_x {ns}.data
scoreboard players operation #off_ny {ns}.data = #normal_y {ns}.data
scoreboard players operation #off_ny {ns}.data *= #offset_y {ns}.data
scoreboard players operation #off_ty {ns}.data = #tangent_y {ns}.data
scoreboard players operation #off_ty {ns}.data *= #offset_z {ns}.data

scoreboard players operation #pos_new_y {ns}.data = #off_by {ns}.data
scoreboard players operation #pos_new_y {ns}.data += #off_ny {ns}.data
scoreboard players operation #pos_new_y {ns}.data += #off_ty {ns}.data
scoreboard players operation #pos_new_y {ns}.data /= #1000 {ns}.data
scoreboard players operation #pos_new_y {ns}.data += #pos_initial_y {ns}.data

scoreboard players operation #off_bz {ns}.data = #binormal_z {ns}.data
scoreboard players operation #off_bz {ns}.data *= #offset_x {ns}.data
scoreboard players operation #off_nz {ns}.data = #normal_z {ns}.data
scoreboard players operation #off_nz {ns}.data *= #offset_y {ns}.data
scoreboard players operation #off_tz {ns}.data = #tangent_z {ns}.data
scoreboard players operation #off_tz {ns}.data *= #offset_z {ns}.data

scoreboard players operation #pos_new_z {ns}.data = #off_bz {ns}.data
scoreboard players operation #pos_new_z {ns}.data += #off_nz {ns}.data
scoreboard players operation #pos_new_z {ns}.data += #off_tz {ns}.data
scoreboard players operation #pos_new_z {ns}.data /= #1000 {ns}.data
scoreboard players operation #pos_new_z {ns}.data += #pos_initial_z {ns}.data
""")

