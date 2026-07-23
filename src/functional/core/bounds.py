
# Shared boundary functions (normalize, load, forceload)
from stewbeet import Mem, write_versioned_function


def write_shared_bounds_functions() -> None:
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		## Load boundaries from mode storage: build the min/max AABB over ALL boundary corners (any
		## count >= 2, any order), then offset by the map base. Folding over every corner — instead
		## of only reading boundaries[0] and boundaries[1] — means the four corners of a rectangular
		## play area (or eight of a cuboid) all Just Work: previously only the first two were used, so
		## an adjacent pair collapsed the box to a thin sliver and the boundary appeared to "do
		## nothing" / kill everywhere. Corners are stored relative to the map base.
		## Usage: function shared/load_bounds {{mode:"multiplayer"}}
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

		## Fold the head corner of {ns}:temp _bnd_corners into the running min (#bound_*1) / max
		## (#bound_*2), then recurse over the tail. Base offset is applied once by the caller after.
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

		## Forceload the boundary area (reads from #bound scores)
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

		## Remove forceload from the boundary area
		write_versioned_function("shared/remove_forceload", f"""
execute store result storage {ns}:temp _fl.x1 int 1 run scoreboard players get #bound_x1 {ns}.data
execute store result storage {ns}:temp _fl.z1 int 1 run scoreboard players get #bound_z1 {ns}.data
execute store result storage {ns}:temp _fl.x2 int 1 run scoreboard players get #bound_x2 {ns}.data
execute store result storage {ns}:temp _fl.z2 int 1 run scoreboard players get #bound_z2 {ns}.data
function {ns}:v{version}/shared/forceload_remove with storage {ns}:temp _fl
""")

		write_versioned_function("shared/forceload_remove", "$forceload remove $(x1) $(z1) $(x2) $(z2)")

		## Shared boundary check: get @s position, compare against #bound_x1/x2/y1/y2/z1/z2 scores.
		## Run as an entity at its position. On out-of-bounds: kills via out_of_world damage.
		## Used by missions and zombies (multiplayer uses bounds_kill for kill-tracking instead).
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
