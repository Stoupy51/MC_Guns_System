
#> mgs:v5.3.0/zombies/store_spawn_abox
#
# @executed	as @n[type=minecraft:marker,tag=mgs.new_spawn]
#
# @within	mgs:v5.3.0/zombies/spawn_setup
#

tag @s add mgs.spawn_has_abox
execute store result score #abx mgs.data run data get storage mgs:temp _spawn.activation_box[0]
execute store result score #aby mgs.data run data get storage mgs:temp _spawn.activation_box[1]
execute store result score #abz mgs.data run data get storage mgs:temp _spawn.activation_box[2]
scoreboard players operation #abx mgs.data += #sx mgs.data
scoreboard players operation #aby mgs.data += #sy mgs.data
scoreboard players operation #abz mgs.data += #sz mgs.data
execute store result storage mgs:temp _abox.x double 1 run scoreboard players get #abx mgs.data
execute store result storage mgs:temp _abox.y double 1 run scoreboard players get #aby mgs.data
execute store result storage mgs:temp _abox.z double 1 run scoreboard players get #abz mgs.data
execute store result storage mgs:temp _abox.dx double 1 run data get storage mgs:temp _spawn.activation_box[3]
execute store result storage mgs:temp _abox.dy double 1 run data get storage mgs:temp _spawn.activation_box[4]
execute store result storage mgs:temp _abox.dz double 1 run data get storage mgs:temp _spawn.activation_box[5]
data modify entity @s data.abox set from storage mgs:temp _abox

