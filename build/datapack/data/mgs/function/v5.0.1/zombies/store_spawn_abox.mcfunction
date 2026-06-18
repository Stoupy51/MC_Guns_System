
#> mgs:v5.0.1/zombies/store_spawn_abox
#
# @within	mgs:v5.0.1/zombies/summon_spawn_iter
#

execute store result score #abx mgs.data run data get storage mgs:temp _spawn_iter[0].activation_box[0]
execute store result score #aby mgs.data run data get storage mgs:temp _spawn_iter[0].activation_box[1]
execute store result score #abz mgs.data run data get storage mgs:temp _spawn_iter[0].activation_box[2]
scoreboard players operation #abx mgs.data += #sx mgs.data
scoreboard players operation #aby mgs.data += #sy mgs.data
scoreboard players operation #abz mgs.data += #sz mgs.data
execute store result storage mgs:temp _abox.x double 1 run scoreboard players get #abx mgs.data
execute store result storage mgs:temp _abox.y double 1 run scoreboard players get #aby mgs.data
execute store result storage mgs:temp _abox.z double 1 run scoreboard players get #abz mgs.data
execute store result storage mgs:temp _abox.dx double 1 run data get storage mgs:temp _spawn_iter[0].activation_box[3]
execute store result storage mgs:temp _abox.dy double 1 run data get storage mgs:temp _spawn_iter[0].activation_box[4]
execute store result storage mgs:temp _abox.dz double 1 run data get storage mgs:temp _spawn_iter[0].activation_box[5]
data modify entity @n[tag=mgs.new_spawn] data.abox set from storage mgs:temp _abox

