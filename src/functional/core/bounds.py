""" Shared boundary functions: min/max folding, forceload, and the out-of-bounds check. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers.probes import Probe


# Functions
def write_shared_bounds_functions() -> None:
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		# Min and max over every boundary corner (2 or more, any order), offset by the base, so 4- and 8-corner areas work.
		write_versioned_function("shared/load_bounds", f"""
$data modify storage {ns}:temp _bnd_corners set from storage {ns}:$(mode) game.map.boundaries

# Min (#bound_*1) and max (#bound_*2) start at the first corner.
execute store result score #bound_x1 {ns}.data run data get storage {ns}:temp _bnd_corners[0][0]
execute store result score #bound_y1 {ns}.data run data get storage {ns}:temp _bnd_corners[0][1]
execute store result score #bound_z1 {ns}.data run data get storage {ns}:temp _bnd_corners[0][2]
scoreboard players operation #bound_x2 {ns}.data = #bound_x1 {ns}.data
scoreboard players operation #bound_y2 {ns}.data = #bound_y1 {ns}.data
scoreboard players operation #bound_z2 {ns}.data = #bound_z1 {ns}.data

# The rest are folded into the running box.
data remove storage {ns}:temp _bnd_corners[0]
execute if data storage {ns}:temp _bnd_corners[0] run function {ns}:v{version}/shared/fold_bounds
data remove storage {ns}:temp _bnd_corners

# Corners are relative to the map base.
scoreboard players operation #bound_x1 {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #bound_y1 {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bound_z1 {ns}.data += #gm_base_z {ns}.data
scoreboard players operation #bound_x2 {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #bound_y2 {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bound_z2 {ns}.data += #gm_base_z {ns}.data
""")

		# Fold the head corner, then recurse over the tail.
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

		write_versioned_function("shared/remove_forceload", f"""
execute store result storage {ns}:temp _fl.x1 int 1 run scoreboard players get #bound_x1 {ns}.data
execute store result storage {ns}:temp _fl.z1 int 1 run scoreboard players get #bound_z1 {ns}.data
execute store result storage {ns}:temp _fl.x2 int 1 run scoreboard players get #bound_x2 {ns}.data
execute store result storage {ns}:temp _fl.z2 int 1 run scoreboard players get #bound_z2 {ns}.data
function {ns}:v{version}/shared/forceload_remove with storage {ns}:temp _fl
""")

		write_versioned_function("shared/forceload_remove", "$forceload remove $(x1) $(z1) $(x2) $(z2)")

		# Run as an entity at its position; missions and zombies use it, multiplayer uses bounds_kill for kill tracking.
		write_versioned_function("shared/check_bounds", f"""
{Probe.pos()}
execute store result score @s {ns}.mp.bx run data get storage {ns}:temp _probe_pos[0]
execute store result score @s {ns}.mp.by run data get storage {ns}:temp _probe_pos[1]
execute store result score @s {ns}.mp.bz run data get storage {ns}:temp _probe_pos[2]

execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run return run damage @s 10000 out_of_world
""")

