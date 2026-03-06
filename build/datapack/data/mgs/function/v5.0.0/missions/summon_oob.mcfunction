
#> mgs:v5.0.0/missions/summon_oob
#
# @within	mgs:v5.0.0/missions/start
#

execute store result score #gm_base_x mgs.data run data get storage mgs:missions game.map.base_coordinates[0]
execute store result score #gm_base_y mgs.data run data get storage mgs:missions game.map.base_coordinates[1]
execute store result score #gm_base_z mgs.data run data get storage mgs:missions game.map.base_coordinates[2]

data modify storage mgs:temp _oob_iter set from storage mgs:missions game.map.out_of_bounds
execute if data storage mgs:temp _oob_iter[0] run function mgs:v5.0.0/missions/summon_oob_iter

