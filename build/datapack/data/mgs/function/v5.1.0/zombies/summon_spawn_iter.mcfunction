
#> mgs:v5.1.0/zombies/summon_spawn_iter
#
# @within	mgs:v5.1.0/zombies/summon_spawns
#			mgs:v5.1.0/zombies/summon_spawn_iter
#

execute store result score #sx mgs.data run data get storage mgs:temp _spawn_iter[0].pos[0]
execute store result score #sy mgs.data run data get storage mgs:temp _spawn_iter[0].pos[1]
execute store result score #sz mgs.data run data get storage mgs:temp _spawn_iter[0].pos[2]
execute store result score #syaw mgs.data run data get storage mgs:temp _spawn_iter[0].rotation[0] 100

scoreboard players operation #sx mgs.data += #gm_base_x mgs.data
scoreboard players operation #sy mgs.data += #gm_base_y mgs.data
scoreboard players operation #sz mgs.data += #gm_base_z mgs.data

execute store result storage mgs:temp _spos.x double 1 run scoreboard players get #sx mgs.data
execute store result storage mgs:temp _spos.y double 1 run scoreboard players get #sy mgs.data
execute store result storage mgs:temp _spos.z double 1 run scoreboard players get #sz mgs.data
execute store result storage mgs:temp _spos.yaw double 0.01 run scoreboard players get #syaw mgs.data
data modify storage mgs:temp _spos.tag set from storage mgs:temp _spawn_tag

function mgs:v5.1.0/zombies/summon_spawn_at with storage mgs:temp _spos

# Defaults to group 0.
scoreboard players set @n[tag=mgs.new_spawn] mgs.zb.spawn.gid 0
execute store result score @n[tag=mgs.new_spawn] mgs.zb.spawn.gid run data get storage mgs:temp _spawn_iter[0].group_id

# Zombies remember their spawn so they never reuse it.
scoreboard players add #zb_spawn_sid mgs.data 1
scoreboard players operation @n[tag=mgs.new_spawn] mgs.zb.spawn.sid = #zb_spawn_sid mgs.data

# Zombie spawns only: the absolute box [x, y, z, dx, dy, dz] (all 6 needed), so a player standing in it gates the spawn.
execute if data storage mgs:temp _spawn_iter[0].activation_box[5] run function mgs:v5.1.0/zombies/store_spawn_abox

# Zombie spawns only: zombies spawned here are escorted to this absolute spot.
execute if data storage mgs:temp _spawn_iter[0].walk_to[2] run function mgs:v5.1.0/zombies/store_spawn_walk_to

tag @n[tag=mgs.new_spawn] remove mgs.new_spawn

data remove storage mgs:temp _spawn_iter[0]
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.1.0/zombies/summon_spawn_iter

