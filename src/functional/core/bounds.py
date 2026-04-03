
# Shared boundary functions (normalize, load, forceload)
from stewbeet import Mem, write_versioned_function


def write_shared_bounds_functions() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Normalize boundaries: ensure min/max ordering for all axes
	write_versioned_function("shared/normalize_bounds", f"""
execute if score #bound_x1 {ns}.data > #bound_x2 {ns}.data run scoreboard players operation #swap {ns}.data = #bound_x1 {ns}.data
execute if score #bound_x1 {ns}.data > #bound_x2 {ns}.data run scoreboard players operation #bound_x1 {ns}.data = #bound_x2 {ns}.data
execute if score #swap {ns}.data matches -2147483648.. run scoreboard players operation #bound_x2 {ns}.data = #swap {ns}.data
execute if score #swap {ns}.data matches -2147483648.. run scoreboard players reset #swap {ns}.data

execute if score #bound_y1 {ns}.data > #bound_y2 {ns}.data run scoreboard players operation #swap {ns}.data = #bound_y1 {ns}.data
execute if score #bound_y1 {ns}.data > #bound_y2 {ns}.data run scoreboard players operation #bound_y1 {ns}.data = #bound_y2 {ns}.data
execute if score #swap {ns}.data matches -2147483648.. run scoreboard players operation #bound_y2 {ns}.data = #swap {ns}.data
execute if score #swap {ns}.data matches -2147483648.. run scoreboard players reset #swap {ns}.data

execute if score #bound_z1 {ns}.data > #bound_z2 {ns}.data run scoreboard players operation #swap {ns}.data = #bound_z1 {ns}.data
execute if score #bound_z1 {ns}.data > #bound_z2 {ns}.data run scoreboard players operation #bound_z1 {ns}.data = #bound_z2 {ns}.data
execute if score #swap {ns}.data matches -2147483648.. run scoreboard players operation #bound_z2 {ns}.data = #swap {ns}.data
execute if score #swap {ns}.data matches -2147483648.. run scoreboard players reset #swap {ns}.data
""")

	## Load boundaries from mode storage and normalize
	## Usage: function shared/load_bounds {{mode:"multiplayer"}}
	write_versioned_function("shared/load_bounds", f"""
$execute store result score #bound_x1 {ns}.data run data get storage {ns}:$(mode) game.map.boundaries[0][0]
$execute store result score #bound_y1 {ns}.data run data get storage {ns}:$(mode) game.map.boundaries[0][1]
$execute store result score #bound_z1 {ns}.data run data get storage {ns}:$(mode) game.map.boundaries[0][2]
$execute store result score #bound_x2 {ns}.data run data get storage {ns}:$(mode) game.map.boundaries[1][0]
$execute store result score #bound_y2 {ns}.data run data get storage {ns}:$(mode) game.map.boundaries[1][1]
$execute store result score #bound_z2 {ns}.data run data get storage {ns}:$(mode) game.map.boundaries[1][2]
scoreboard players operation #bound_x1 {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #bound_y1 {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bound_z1 {ns}.data += #gm_base_z {ns}.data
scoreboard players operation #bound_x2 {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #bound_y2 {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bound_z2 {ns}.data += #gm_base_z {ns}.data
function {ns}:v{version}/shared/normalize_bounds
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

