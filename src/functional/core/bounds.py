""" Shared boundary functions: min/max folding, forceload, and the out-of-bounds check. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_shared_bounds_functions() -> None:
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		# Build the min/max AABB over ALL boundary corners (any count >= 2, any order), then offset by the base.
		# Folding every corner is what makes 4- or 8-corner areas work.
		# Reading only boundaries[0..1] collapsed an adjacent pair into a sliver that killed everywhere.
		write_versioned_function("shared/load_bounds", f"""
$data modify storage {ns}:temp _bnd_corners set from storage {ns}:$(mode) game.map.boundaries

# Seed both min (#bound_*1) and max (#bound_*2) from the first corner
execute store result score #bound_x1 {ns}.data run data get storage {ns}:temp _bnd_corners[0][0]
execute store result score #bound_y1 {ns}.data run data get storage {ns}:temp _bnd_corners[0][1]
execute store result score #bound_z1 {ns}.data run data get storage {ns}:temp _bnd_corners[0][2]
scoreboard players operation #bound_x2 {ns}.data = #bound_x1 {ns}.data
scoreboard players operation #bound_y2 {ns}.data = #bound_y1 {ns}.data
scoreboard players operation #bound_z2 {ns}.data = #bound_z1 {ns}.data

# Fold every remaining corner into the running min/max box (already ordered, so no normalize needed)
data remove storage {ns}:temp _bnd_corners[0]
execute if data storage {ns}:temp _bnd_corners[0] run function {ns}:v{version}/shared/fold_bounds
data remove storage {ns}:temp _bnd_corners

# Offset the whole box by the map base (corners are stored relative to it)
scoreboard players operation #bound_x1 {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #bound_y1 {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bound_z1 {ns}.data += #gm_base_z {ns}.data
scoreboard players operation #bound_x2 {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #bound_y2 {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bound_z2 {ns}.data += #gm_base_z {ns}.data
""")

		# Fold the head corner into the running min/max, then recurse over the tail
		write_versioned_function("shared/fold_bounds", f"""
execute store result score #bc_x {ns}.data run data get storage {ns}:temp _bnd_corners[0][0]
execute store result score #bc_y {ns}.data run data get storage {ns}:temp _bnd_corners[0][1]
execute store result score #bc_z {ns}.data run data get storage {ns}:temp _bnd_corners[0][2]
execute if score #bc_x {ns}.data < #bound_x1 {ns}.data run scoreboard players operation #bound_x1 {ns}.data = #bc_x {ns}.data
execute if score #bc_x {ns}.data > #bound_x2 {ns}.data run scoreboard players operation #bound_x2 {ns}.data = #bc_x {ns}.data
execute if score #bc_y {ns}.data < #bound_y1 {ns}.data run scoreboard players operation #bound_y1 {ns}.data = #bc_y {ns}.data
execute if score #bc_y {ns}.data > #bound_y2 {ns}.data run scoreboard players operation #bound_y2 {ns}.data = #bc_y {ns}.data
execute if score #bc_z {ns}.data < #bound_z1 {ns}.data run scoreboard players operation #bound_z1 {ns}.data = #bc_z {ns}.data
execute if score #bc_z {ns}.data > #bound_z2 {ns}.data run scoreboard players operation #bound_z2 {ns}.data = #bc_z {ns}.data
data remove storage {ns}:temp _bnd_corners[0]
execute if data storage {ns}:temp _bnd_corners[0] run function {ns}:v{version}/shared/fold_bounds
""")

		# Forceload the boundary area, read from the #bound scores
		write_versioned_function("shared/forceload_area", f"""
execute store result storage {ns}:temp _fl.x1 int 1 run scoreboard players get #bound_x1 {ns}.data
execute store result storage {ns}:temp _fl.z1 int 1 run scoreboard players get #bound_z1 {ns}.data
execute store result storage {ns}:temp _fl.x2 int 1 run scoreboard players get #bound_x2 {ns}.data
execute store result storage {ns}:temp _fl.z2 int 1 run scoreboard players get #bound_z2 {ns}.data
function {ns}:v{version}/shared/forceload_add with storage {ns}:temp _fl
""")

		write_versioned_function("shared/forceload_add", """
$forceload add $(x1) $(z1) $(x2) $(z2)
""")

		# Remove forceload from the boundary area
		write_versioned_function("shared/remove_forceload", f"""
execute store result storage {ns}:temp _fl.x1 int 1 run scoreboard players get #bound_x1 {ns}.data
execute store result storage {ns}:temp _fl.z1 int 1 run scoreboard players get #bound_z1 {ns}.data
execute store result storage {ns}:temp _fl.x2 int 1 run scoreboard players get #bound_x2 {ns}.data
execute store result storage {ns}:temp _fl.z2 int 1 run scoreboard players get #bound_z2 {ns}.data
function {ns}:v{version}/shared/forceload_remove with storage {ns}:temp _fl
""")

		write_versioned_function("shared/forceload_remove", "$forceload remove $(x1) $(z1) $(x2) $(z2)")

		# Compare @s against the #bound scores and kill on exit; run as an entity at its position.
		# Missions and zombies use this, multiplayer uses bounds_kill for kill-tracking instead.
		write_versioned_function("shared/check_bounds", f"""
data modify storage {ns}:temp _player_pos set from entity @s Pos
execute store result score @s {ns}.mp.bx run data get storage {ns}:temp _player_pos[0]
execute store result score @s {ns}.mp.by run data get storage {ns}:temp _player_pos[1]
execute store result score @s {ns}.mp.bz run data get storage {ns}:temp _player_pos[2]

execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run return run damage @s 10000 out_of_world
""")

