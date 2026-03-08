
#> mgs:v5.0.0/zombies/mystery_box/setup_pos_iter
#
# @within	mgs:v5.0.0/zombies/mystery_box/setup_positions
#			mgs:v5.0.0/zombies/mystery_box/setup_pos_iter
#

execute store result score #_mbx mgs.data run data get storage mgs:temp _mb_iter[0][0]
execute store result score #_mby mgs.data run data get storage mgs:temp _mb_iter[0][1]
execute store result score #_mbz mgs.data run data get storage mgs:temp _mb_iter[0][2]

scoreboard players operation #_mbx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_mby mgs.data += #gm_base_y mgs.data
scoreboard players operation #_mbz mgs.data += #gm_base_z mgs.data

execute store result storage mgs:temp _mbpos.x double 1 run scoreboard players get #_mbx mgs.data
execute store result storage mgs:temp _mbpos.y double 1 run scoreboard players get #_mby mgs.data
execute store result storage mgs:temp _mbpos.z double 1 run scoreboard players get #_mbz mgs.data

function mgs:v5.0.0/zombies/mystery_box/summon_pos_at with storage mgs:temp _mbpos

data remove storage mgs:temp _mb_iter[0]
execute if data storage mgs:temp _mb_iter[0] run function mgs:v5.0.0/zombies/mystery_box/setup_pos_iter

