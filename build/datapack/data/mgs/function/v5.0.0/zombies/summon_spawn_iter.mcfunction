
#> mgs:v5.0.0/zombies/summon_spawn_iter
#
# @within	mgs:v5.0.0/zombies/summon_spawns
#			mgs:v5.0.0/zombies/summon_spawn_iter
#

execute store result score #_sx mgs.data run data get storage mgs:temp _spawn_iter[0][0]
execute store result score #_sy mgs.data run data get storage mgs:temp _spawn_iter[0][1]
execute store result score #_sz mgs.data run data get storage mgs:temp _spawn_iter[0][2]
execute store result score #_syaw mgs.data run data get storage mgs:temp _spawn_iter[0][3] 100

scoreboard players operation #_sx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_sy mgs.data += #gm_base_y mgs.data
scoreboard players operation #_sz mgs.data += #gm_base_z mgs.data

execute store result storage mgs:temp _spos.x double 1 run scoreboard players get #_sx mgs.data
execute store result storage mgs:temp _spos.y double 1 run scoreboard players get #_sy mgs.data
execute store result storage mgs:temp _spos.z double 1 run scoreboard players get #_sz mgs.data
execute store result storage mgs:temp _spos.yaw double 0.01 run scoreboard players get #_syaw mgs.data
data modify storage mgs:temp _spos.tag set from storage mgs:temp _spawn_tag

function mgs:v5.0.0/zombies/summon_spawn_at with storage mgs:temp _spos

data remove storage mgs:temp _spawn_iter[0]
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/zombies/summon_spawn_iter

