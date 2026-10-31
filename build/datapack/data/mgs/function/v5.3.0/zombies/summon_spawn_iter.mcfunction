
#> mgs:v5.3.0/zombies/summon_spawn_iter
#
# @within	mgs:v5.3.0/zombies/summon_spawns
#			mgs:v5.3.0/zombies/summon_spawn_iter
#

# The kind's defaults stand in for the fields the map leaves out.
data modify storage mgs:temp _spawn set from storage mgs:temp _spawn_defaults
data modify storage mgs:temp _spawn merge from storage mgs:temp _spawn_iter[0]

execute store result score #sx mgs.data run data get storage mgs:temp _spawn.pos[0]
execute store result score #sy mgs.data run data get storage mgs:temp _spawn.pos[1]
execute store result score #sz mgs.data run data get storage mgs:temp _spawn.pos[2]
execute store result score #syaw mgs.data run data get storage mgs:temp _spawn.rotation[0] 100

scoreboard players operation #sx mgs.data += #gm_base_x mgs.data
scoreboard players operation #sy mgs.data += #gm_base_y mgs.data
scoreboard players operation #sz mgs.data += #gm_base_z mgs.data

execute store result storage mgs:temp _spos.x double 1 run scoreboard players get #sx mgs.data
execute store result storage mgs:temp _spos.y double 1 run scoreboard players get #sy mgs.data
execute store result storage mgs:temp _spos.z double 1 run scoreboard players get #sz mgs.data
execute store result storage mgs:temp _spos.yaw double 0.01 run scoreboard players get #syaw mgs.data
data modify storage mgs:temp _spos.tag set from storage mgs:temp _spawn_tag

# "Zombie Spawn #12 (group 2)": zombies remember their spawn's id so the stuck rescue never reuses it.
scoreboard players add #zb_spawn_sid mgs.data 1
data modify storage mgs:temp _spawn_label set value {group_id:0}
data modify storage mgs:temp _spawn_label.name set from storage mgs:temp _spawn_name
data modify storage mgs:temp _spawn_label.group_id set from storage mgs:temp _spawn.group_id
execute store result storage mgs:temp _spawn_label.sid int 1 run scoreboard players get #zb_spawn_sid mgs.data
function mgs:v5.3.0/zombies/spawn_name with storage mgs:temp _spawn_label

function mgs:v5.3.0/zombies/summon_spawn_at with storage mgs:temp _spos
execute as @n[type=minecraft:marker,tag=mgs.new_spawn] run function mgs:v5.3.0/zombies/spawn_setup

data remove storage mgs:temp _spawn_iter[0]
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.3.0/zombies/summon_spawn_iter

