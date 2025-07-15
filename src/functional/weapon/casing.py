
# Imports
from stewbeet import Mem, write_versioned_function

from ...config.stats import CASING_BINORMAL, CASING_MODEL, CASING_NORMAL, CASING_OFFSET, CASING_TANGENT


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Handle pending clicks
    write_versioned_function("player/right_click",
f"""
# Drop casing
function {ns}:v{version}/casing/main
""")

    # Prepare
    item_nbt: str = f"""{{Tags:["{ns}.new","{ns}.casing"],Item:{{id:"minecraft:stone",count:1,components:{{"minecraft:item_model":"air"}}}},PickupDelay:32767,Age:5990}}"""

    # Main function
    write_versioned_function("casing/main",
f"""
# Get if player is zooming or not
scoreboard players set #is_zoom {ns}.data 0
execute if data storage {ns}:gun all.stats.is_zoom run scoreboard players set #is_zoom {ns}.data 1

# Extract casing data from gun
scoreboard players set #casing_normal {ns}.data 0
scoreboard players set #casing_tangent {ns}.data 0
scoreboard players set #casing_binormal {ns}.data 0
execute store result score #casing_normal {ns}.data run data get storage {ns}:gun all.stats.{CASING_NORMAL}
execute store result score #casing_tangent {ns}.data run data get storage {ns}:gun all.stats.{CASING_TANGENT}
execute store result score #casing_binormal {ns}.data run data get storage {ns}:gun all.stats.{CASING_BINORMAL}

# Stop if no casing data
execute unless data storage {ns}:gun all.stats.{CASING_MODEL} run return fail

# Add random variation to the tangent
scoreboard players set #random_variation {ns}.data 40
execute store result score #random_variation {ns}.data run random value 0..39
scoreboard players remove #random_variation {ns}.data 20
scoreboard players operation #casing_tangent {ns}.data += #random_variation {ns}.data

# Calculate look vectors and motion
execute anchored eyes positioned ^ ^ ^ summon marker run function {ns}:v{version}/casing/process_vectors

# Prepare casting model and motion
data modify storage {ns}:temp casing set value {{Item:{{components:{{}}}},Motion:[0.0d,0.0d,0.0d],Pos:[0.0d,0.0d,0.0d]}}
data modify storage {ns}:temp casing.Item.components."minecraft:item_model" set from storage {ns}:gun all.stats.{CASING_MODEL}
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
    write_versioned_function("casing/update_item",
f"""
data modify entity @s {{}} merge from storage {ns}:temp casing
tag @s remove {ns}.new
""")

    # Process vectors - main handler that calls the 3 sub-functions
    write_versioned_function("casing/process_vectors",
f"""
# 1. Calculate base vectors
function {ns}:v{version}/casing/calculate_vectors

# 2. Calculate motion based on these vectors
function {ns}:v{version}/casing/calculate_motion

# 3. Calculate position offset based on these vectors
function {ns}:v{version}/casing/calculate_offset

# 4. Kill marker
kill @s
""")

    # 1. Calculate normal, tangent, and binormal vectors
    write_versioned_function("casing/calculate_vectors",
f"""
### Calculate base vectors (normal, tangent, binormal) from player's look direction

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
""")

    # 2. Calculate motion based on vectors
    write_versioned_function("casing/calculate_motion",
f"""
### Calculate motion based on scaled normal, tangent, and binormal vectors

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
""")

    # 3. Calculate offset based on vectors
    write_versioned_function("casing/calculate_offset",
f"""
### Transform local casing offsets into world-space coordinates using the gun's orientation vectors

# 1) Load local offset values from storage and scale to integers (x1000)
# These represent the desired offset in the gun's local coordinate system
execute if score #is_zoom {ns}.data matches 0 store result score #offset_x {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.normal[0] 1000
execute if score #is_zoom {ns}.data matches 0 store result score #offset_y {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.normal[1] 1000
execute if score #is_zoom {ns}.data matches 0 store result score #offset_z {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.normal[2] 1000
execute if score #is_zoom {ns}.data matches 1 store result score #offset_x {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.zoom[0] 1000
execute if score #is_zoom {ns}.data matches 1 store result score #offset_y {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.zoom[1] 1000
execute if score #is_zoom {ns}.data matches 1 store result score #offset_z {ns}.data run data get storage {ns}:gun all.stats.{CASING_OFFSET}.zoom[2] 1000

# 2) Project local offsets onto world-space axes using orientation vectors
# Each vector (binormal/normal/tangent) contributes to the final world position
# Binormal vector (local X) contribution
scoreboard players operation #off_bx {ns}.data = #binormal_x {ns}.data
scoreboard players operation #off_bx {ns}.data *= #offset_x {ns}.data
# Normal vector (local Y) contribution
scoreboard players operation #off_nx {ns}.data = #normal_x {ns}.data
scoreboard players operation #off_nx {ns}.data *= #offset_y {ns}.data
# Tangent vector (local Z) contribution
scoreboard players operation #off_tx {ns}.data = #tangent_x {ns}.data
scoreboard players operation #off_tx {ns}.data *= #offset_z {ns}.data

# 3) Combine vector contributions and convert back to decimal coordinates
# Sum all contributions for X coordinate
scoreboard players operation #pos_new_x {ns}.data = #off_bx {ns}.data
scoreboard players operation #pos_new_x {ns}.data += #off_nx {ns}.data
scoreboard players operation #pos_new_x {ns}.data += #off_tx {ns}.data
scoreboard players operation #pos_new_x {ns}.data /= #1000 {ns}.data

# 4) Add base position to get final world coordinates
scoreboard players operation #pos_new_x {ns}.data += #pos_initial_x {ns}.data

# Repeat same process for Y coordinate
# Project local offsets onto world Y axis
scoreboard players operation #off_by {ns}.data = #binormal_y {ns}.data
scoreboard players operation #off_by {ns}.data *= #offset_x {ns}.data
scoreboard players operation #off_ny {ns}.data = #normal_y {ns}.data
scoreboard players operation #off_ny {ns}.data *= #offset_y {ns}.data
scoreboard players operation #off_ty {ns}.data = #tangent_y {ns}.data
scoreboard players operation #off_ty {ns}.data *= #offset_z {ns}.data

# Combine and convert Y coordinate
scoreboard players operation #pos_new_y {ns}.data = #off_by {ns}.data
scoreboard players operation #pos_new_y {ns}.data += #off_ny {ns}.data
scoreboard players operation #pos_new_y {ns}.data += #off_ty {ns}.data
scoreboard players operation #pos_new_y {ns}.data /= #1000 {ns}.data
scoreboard players operation #pos_new_y {ns}.data += #pos_initial_y {ns}.data

# Repeat same process for Z coordinate
# Project local offsets onto world Z axis
scoreboard players operation #off_bz {ns}.data = #binormal_z {ns}.data
scoreboard players operation #off_bz {ns}.data *= #offset_x {ns}.data
scoreboard players operation #off_nz {ns}.data = #normal_z {ns}.data
scoreboard players operation #off_nz {ns}.data *= #offset_y {ns}.data
scoreboard players operation #off_tz {ns}.data = #tangent_z {ns}.data
scoreboard players operation #off_tz {ns}.data *= #offset_z {ns}.data

# Combine and convert Z coordinate
scoreboard players operation #pos_new_z {ns}.data = #off_bz {ns}.data
scoreboard players operation #pos_new_z {ns}.data += #off_nz {ns}.data
scoreboard players operation #pos_new_z {ns}.data += #off_tz {ns}.data
scoreboard players operation #pos_new_z {ns}.data /= #1000 {ns}.data
scoreboard players operation #pos_new_z {ns}.data += #pos_initial_z {ns}.data
""")

