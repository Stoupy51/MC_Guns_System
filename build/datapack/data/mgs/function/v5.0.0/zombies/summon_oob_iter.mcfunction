
#> mgs:v5.0.0/zombies/summon_oob_iter
#
# @within	mgs:v5.0.0/zombies/summon_oob
#			mgs:v5.0.0/zombies/summon_oob_iter
#

execute store result score #rx mgs.data run data get storage mgs:temp _oob_iter[0][0]
execute store result score #ry mgs.data run data get storage mgs:temp _oob_iter[0][1]
execute store result score #rz mgs.data run data get storage mgs:temp _oob_iter[0][2]
scoreboard players operation #rx mgs.data += #gm_base_x mgs.data
scoreboard players operation #ry mgs.data += #gm_base_y mgs.data
scoreboard players operation #rz mgs.data += #gm_base_z mgs.data
execute store result storage mgs:temp _oob_pos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _oob_pos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _oob_pos.z double 1 run scoreboard players get #rz mgs.data
function mgs:v5.0.0/zombies/summon_oob_at with storage mgs:temp _oob_pos
data remove storage mgs:temp _oob_iter[0]
execute if data storage mgs:temp _oob_iter[0] run function mgs:v5.0.0/zombies/summon_oob_iter

