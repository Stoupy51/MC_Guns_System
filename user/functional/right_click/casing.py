
# Imports
from python_datapack.utils.database_helper import write_versioned_function

from user.config.stats import CASING_BINORMAL, CASING_MODEL, CASING_NORMAL, CASING_OFFSET, CASING_TANGENT


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Drop casing
function {ns}:v{version}/casing/main
""")

    # Prepare
    item_nbt: str = f"""{{Tags:["{ns}.new","{ns}.casing"],Item:{{id:"minecraft:stone",count:1,components:{{"minecraft:item_model":"air"}}}},PickupDelay:32767,Age:5990}}"""

    # Main function
    write_versioned_function(config, "casing/main",
f"""
# Extract casing data from gun
scoreboard players set #casing_normal {ns}.data 0
scoreboard players set #casing_tangent {ns}.data 0
scoreboard players set #casing_binormal {ns}.data 0
execute store result score #casing_normal {ns}.data run data get storage {ns}:gun stats.{CASING_NORMAL}
execute store result score #casing_tangent {ns}.data run data get storage {ns}:gun stats.{CASING_TANGENT}
execute store result score #casing_binormal {ns}.data run data get storage {ns}:gun stats.{CASING_BINORMAL}

# Stop if no casing data
execute unless data storage {ns}:gun stats.{CASING_MODEL} run return fail

# Add random variation to the tangent
scoreboard players set #random_variation {ns}.data 40
execute store result score #random_variation {ns}.data run random value 0..39
scoreboard players remove #random_variation {ns}.data 20
scoreboard players operation #casing_tangent {ns}.data += #random_variation {ns}.data

# Calculate look vectors
execute anchored eyes positioned ^ ^ ^ summon marker run function {ns}:v{version}/casing/look_vectors

# Prepare casting model and motion
data modify storage {ns}:temp casing set value {{Item:{{components:{{}}}},Motion:[0.0d,0.0d,0.0d],Pos:[0.0d,0.0d,0.0d]}}
data modify storage {ns}:temp casing.Item.components."minecraft:item_model" set from storage {ns}:gun stats.{CASING_MODEL}
execute store result storage {ns}:temp casing.Motion[0] double 0.001 run scoreboard players get #motion_x {ns}.data
execute store result storage {ns}:temp casing.Motion[1] double 0.001 run scoreboard players get #motion_y {ns}.data
execute store result storage {ns}:temp casing.Motion[2] double 0.001 run scoreboard players get #motion_z {ns}.data

# Prepare position offset
execute store result storage {ns}:temp casing.Pos[0] double 0.001 run scoreboard players get #pos_new_x {ns}.data
execute store result storage {ns}:temp casing.Pos[1] double 0.001 run scoreboard players get #pos_new_y {ns}.data
execute store result storage {ns}:temp casing.Pos[2] double 0.001 run scoreboard players get #pos_new_z {ns}.data

# Create casing entity
summon item ~ ~ ~ {item_nbt}
execute as @n[type=item,tag={ns}.new] run function {ns}:v{version}/casing/update_item
""")

    # Apply updates to the item
    write_versioned_function(config, "casing/update_item",
f"""
data modify entity @s {{}} merge from storage {ns}:temp casing
tag @s remove {ns}.new
""")

    # Calculate motion vectors
    write_versioned_function(config, "casing/look_vectors",
f"""
### Calculate motion vectors based on look direction and casing parameters

# Store the initial position of the marker (before movement)
tp @s ~ ~ ~ ~ ~
execute store result score #pos_initial_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #pos_initial_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #pos_initial_z {ns}.data run data get entity @s Pos[2] 1000

## --- NORMAL VECTOR (Vertical / Y-axis component) ---

# Move the marker 1 block up relative to its local axes
tp @s ^ ^1 ^

# Calculate the normal vector: difference between new position and initial
execute store result score #normal_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #normal_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #normal_z {ns}.data run data get entity @s Pos[2] 1000
scoreboard players operation #normal_x {ns}.data -= #pos_initial_x {ns}.data
scoreboard players operation #normal_y {ns}.data -= #pos_initial_y {ns}.data
scoreboard players operation #normal_z {ns}.data -= #pos_initial_z {ns}.data

# Scale into a new set of objectives so raw normals stay intact
scoreboard players operation #scaled_normal_x {ns}.data = #normal_x {ns}.data
scoreboard players operation #scaled_normal_x {ns}.data *= #casing_normal {ns}.data
scoreboard players operation #scaled_normal_y {ns}.data = #normal_y {ns}.data
scoreboard players operation #scaled_normal_y {ns}.data *= #casing_normal {ns}.data
scoreboard players operation #scaled_normal_z {ns}.data = #normal_z {ns}.data
scoreboard players operation #scaled_normal_z {ns}.data *= #casing_normal {ns}.data

## --- TANGENT VECTOR (Forward / Z-axis component) ---

# Move the marker 1 block forward (local Z)
tp @s ^ ^ ^1
execute store result score #tangent_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #tangent_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #tangent_z {ns}.data run data get entity @s Pos[2] 1000
scoreboard players operation #tangent_x {ns}.data -= #pos_initial_x {ns}.data
scoreboard players operation #tangent_y {ns}.data -= #pos_initial_y {ns}.data
scoreboard players operation #tangent_z {ns}.data -= #pos_initial_z {ns}.data

# Preserve raw tangents, then scale
scoreboard players operation #scaled_tangent_x {ns}.data = #tangent_x {ns}.data
scoreboard players operation #scaled_tangent_x {ns}.data *= #casing_tangent {ns}.data
scoreboard players operation #scaled_tangent_y {ns}.data = #tangent_y {ns}.data
scoreboard players operation #scaled_tangent_y {ns}.data *= #casing_tangent {ns}.data
scoreboard players operation #scaled_tangent_z {ns}.data = #tangent_z {ns}.data
scoreboard players operation #scaled_tangent_z {ns}.data *= #casing_tangent {ns}.data

## --- BINORMAL VECTOR (Sideways / X-axis component) ---

# Move the marker 1 block to the right (local X)
tp @s ^1 ^ ^
execute store result score #binormal_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #binormal_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #binormal_z {ns}.data run data get entity @s Pos[2] 1000
scoreboard players operation #binormal_x {ns}.data -= #pos_initial_x {ns}.data
scoreboard players operation #binormal_y {ns}.data -= #pos_initial_y {ns}.data
scoreboard players operation #binormal_z {ns}.data -= #pos_initial_z {ns}.data

# Preserve raw binormals, then scale
scoreboard players operation #scaled_binormal_x {ns}.data = #binormal_x {ns}.data
scoreboard players operation #scaled_binormal_x {ns}.data *= #casing_binormal {ns}.data
scoreboard players operation #scaled_binormal_y {ns}.data = #binormal_y {ns}.data
scoreboard players operation #scaled_binormal_y {ns}.data *= #casing_binormal {ns}.data
scoreboard players operation #scaled_binormal_z {ns}.data = #binormal_z {ns}.data
scoreboard players operation #scaled_binormal_z {ns}.data *= #casing_binormal {ns}.data

## --- COMBINE SCALED VECTORS INTO FINAL MOTION ---

# Start from scaled normals
scoreboard players operation #motion_x {ns}.data = #scaled_normal_x {ns}.data
scoreboard players operation #motion_y {ns}.data = #scaled_normal_y {ns}.data
scoreboard players operation #motion_z {ns}.data = #scaled_normal_z {ns}.data

# Add scaled tangent
scoreboard players operation #motion_x {ns}.data += #scaled_tangent_x {ns}.data
scoreboard players operation #motion_y {ns}.data += #scaled_tangent_y {ns}.data
scoreboard players operation #motion_z {ns}.data += #scaled_tangent_z {ns}.data

# Add scaled binormal
scoreboard players operation #motion_x {ns}.data += #scaled_binormal_x {ns}.data
scoreboard players operation #motion_z {ns}.data += #scaled_binormal_z {ns}.data

## --- SCALE DOWN COMBINED VECTOR ---

# Since vectors are scaled integers (x1000), we need to divide to normalize
scoreboard players operation #motion_x {ns}.data /= #1000 {ns}.data
scoreboard players operation #motion_y {ns}.data /= #1000 {ns}.data
scoreboard players operation #motion_z {ns}.data /= #1000 {ns}.data



## Calculate new position vectors based on normal, tangent, binormal and casing offsets

# 1) Load raw offset values (each *1000 in scoreboard)
execute store result score #offset_x {ns}.data run data get storage {ns}:gun stats.{CASING_OFFSET}[0] 1000
execute store result score #offset_y {ns}.data run data get storage {ns}:gun stats.{CASING_OFFSET}[1] 1000
execute store result score #offset_z {ns}.data run data get storage {ns}:gun stats.{CASING_OFFSET}[2] 1000

# 2) Compute each axis' contribution to world-space offset
# Binormal (X-axis)
scoreboard players operation #off_bx {ns}.data = #binormal_x {ns}.data
scoreboard players operation #off_bx {ns}.data *= #offset_x {ns}.data
# Normal   (Y-axis)
scoreboard players operation #off_nx {ns}.data = #normal_x {ns}.data
scoreboard players operation #off_nx {ns}.data *= #offset_y {ns}.data
# Tangent  (Z-axis)
scoreboard players operation #off_tx {ns}.data = #tangent_x {ns}.data
scoreboard players operation #off_tx {ns}.data *= #offset_z {ns}.data

# 3) Sum them and scale down (we did multiply by 1000)
scoreboard players operation #pos_new_x {ns}.data = #off_bx {ns}.data
scoreboard players operation #pos_new_x {ns}.data += #off_nx {ns}.data
scoreboard players operation #pos_new_x {ns}.data += #off_tx {ns}.data
scoreboard players operation #pos_new_x {ns}.data /= #1000 {ns}.data

# 4) Add original position
scoreboard players operation #pos_new_x {ns}.data += #pos_initial_x {ns}.data

# Repeat X logic for Y and Z…

# Y contributions
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

# Z contributions
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

