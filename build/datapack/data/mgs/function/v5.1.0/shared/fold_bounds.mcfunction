
#> mgs:v5.1.0/shared/fold_bounds
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/shared/load_bounds
#			mgs:v5.1.0/shared/fold_bounds
#

execute store result score #bc_x mgs.data run data get storage mgs:temp _bnd_corners[0][0]
execute store result score #bc_y mgs.data run data get storage mgs:temp _bnd_corners[0][1]
execute store result score #bc_z mgs.data run data get storage mgs:temp _bnd_corners[0][2]
execute if score #bc_x mgs.data < #bound_x1 mgs.data run scoreboard players operation #bound_x1 mgs.data = #bc_x mgs.data
execute if score #bc_x mgs.data > #bound_x2 mgs.data run scoreboard players operation #bound_x2 mgs.data = #bc_x mgs.data
execute if score #bc_y mgs.data < #bound_y1 mgs.data run scoreboard players operation #bound_y1 mgs.data = #bc_y mgs.data
execute if score #bc_y mgs.data > #bound_y2 mgs.data run scoreboard players operation #bound_y2 mgs.data = #bc_y mgs.data
execute if score #bc_z mgs.data < #bound_z1 mgs.data run scoreboard players operation #bound_z1 mgs.data = #bc_z mgs.data
execute if score #bc_z mgs.data > #bound_z2 mgs.data run scoreboard players operation #bound_z2 mgs.data = #bc_z mgs.data
data remove storage mgs:temp _bnd_corners[0]
execute if data storage mgs:temp _bnd_corners[0] run function mgs:v5.1.0/shared/fold_bounds

