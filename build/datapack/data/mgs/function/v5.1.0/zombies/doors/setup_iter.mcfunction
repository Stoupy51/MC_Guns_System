
#> mgs:v5.1.0/zombies/doors/setup_iter
#
# @within	mgs:v5.1.0/zombies/doors/setup
#			mgs:v5.1.0/zombies/doors/setup_iter
#

execute store result score #dx mgs.data run data get storage mgs:temp _door_iter[0].pos[0]
execute store result score #dy mgs.data run data get storage mgs:temp _door_iter[0].pos[1]
execute store result score #dz mgs.data run data get storage mgs:temp _door_iter[0].pos[2]
scoreboard players operation #dx mgs.data += #gm_base_x mgs.data
scoreboard players operation #dy mgs.data += #gm_base_y mgs.data
scoreboard players operation #dz mgs.data += #gm_base_z mgs.data

execute store result storage mgs:temp _door.x int 1 run scoreboard players get #dx mgs.data
execute store result storage mgs:temp _door.y int 1 run scoreboard players get #dy mgs.data
execute store result storage mgs:temp _door.z int 1 run scoreboard players get #dz mgs.data
data modify storage mgs:temp _door.block set from storage mgs:temp _door_iter[0].block
data modify storage mgs:temp _door.facing set value 0
execute store result storage mgs:temp _door.facing int 1 run data get storage mgs:temp _door_iter[0].rotation[0]

# Name defaults to "Door".
data modify storage mgs:temp _door_name.name set value "Door"
execute if data storage mgs:temp _door_iter[0].name run data modify storage mgs:temp _door_name.name set from storage mgs:temp _door_iter[0].name
# back_name defaults to the name.
data modify storage mgs:temp _door_name.back_name set from storage mgs:temp _door_name.name
execute if data storage mgs:temp _door_iter[0].back_name run data modify storage mgs:temp _door_name.back_name set from storage mgs:temp _door_iter[0].back_name

function mgs:v5.1.0/zombies/doors/place_at with storage mgs:temp _door

execute store result score @e[tag=mgs.door_new] mgs.zb.door.link run data get storage mgs:temp _door_iter[0].link_id
execute store result score @e[tag=mgs.door_new] mgs.zb.door.price run data get storage mgs:temp _door_iter[0].price
execute store result score @e[tag=mgs.door_new] mgs.zb.door.bgid run data get storage mgs:temp _door_iter[0].back_group_id
execute store result score @e[tag=mgs.door_new] mgs.zb.door.anim run data get storage mgs:temp _door_iter[0].animation
execute store result score @e[tag=mgs.door_new] mgs.zb.door.rot run data get storage mgs:temp _door_iter[0].rotation[0]

# Maps saved before chip-in existed have no field: the failed read stores 0 (off).
scoreboard players set @e[tag=mgs.door_new] mgs.zb.door.paid 0
execute store result score @e[tag=mgs.door_new] mgs.zb.door.partial run data get storage mgs:temp _door_iter[0].partial_price

execute store result storage mgs:temp _door_name.id int 1 run data get storage mgs:temp _door_iter[0].link_id
function mgs:v5.1.0/zombies/doors/store_name with storage mgs:temp _door_name

execute as @e[tag=mgs.door_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.1.0/zombies/doors/on_right_click",executor:"source"}
execute as @e[tag=mgs.door_new] run function #bs.interaction:on_hover {run:"function mgs:v5.1.0/zombies/doors/on_hover",executor:"source"}
tag @e[tag=mgs.door_new] remove mgs.door_new

data remove storage mgs:temp _door_iter[0]
execute if data storage mgs:temp _door_iter[0] run function mgs:v5.1.0/zombies/doors/setup_iter

