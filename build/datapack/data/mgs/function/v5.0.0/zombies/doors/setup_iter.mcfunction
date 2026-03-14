
#> mgs:v5.0.0/zombies/doors/setup_iter
#
# @within	mgs:v5.0.0/zombies/doors/setup
#			mgs:v5.0.0/zombies/doors/setup_iter
#

# Read relative position and convert to absolute
execute store result score #dx mgs.data run data get storage mgs:temp _door_iter[0].pos[0]
execute store result score #dy mgs.data run data get storage mgs:temp _door_iter[0].pos[1]
execute store result score #dz mgs.data run data get storage mgs:temp _door_iter[0].pos[2]
scoreboard players operation #dx mgs.data += #gm_base_x mgs.data
scoreboard players operation #dy mgs.data += #gm_base_y mgs.data
scoreboard players operation #dz mgs.data += #gm_base_z mgs.data

# Store absolute position and block for macro
execute store result storage mgs:temp _door.x int 1 run scoreboard players get #dx mgs.data
execute store result storage mgs:temp _door.y int 1 run scoreboard players get #dy mgs.data
execute store result storage mgs:temp _door.z int 1 run scoreboard players get #dz mgs.data
data modify storage mgs:temp _door.block set from storage mgs:temp _door_iter[0].block

# Read door name (default "Door", override with "name" field)
data modify storage mgs:temp _door_name.name set value "Door"
execute if data storage mgs:temp _door_iter[0].name run data modify storage mgs:temp _door_name.name set from storage mgs:temp _door_iter[0].name
# Read optional back_name (default to name)
data modify storage mgs:temp _door_name.back_name set from storage mgs:temp _door_name.name
execute if data storage mgs:temp _door_iter[0].back_name run data modify storage mgs:temp _door_name.back_name set from storage mgs:temp _door_iter[0].back_name

# Place block and summon interaction entity
function mgs:v5.0.0/zombies/doors/place_at with storage mgs:temp _door

# Set scoreboards on newly spawned door entity
execute store result score @n[tag=mgs.door_new] mgs.zb.door.link run data get storage mgs:temp _door_iter[0].link_id
execute store result score @n[tag=mgs.door_new] mgs.zb.door.price run data get storage mgs:temp _door_iter[0].price
execute store result score @n[tag=mgs.door_new] mgs.zb.door.gid run data get storage mgs:temp _door_iter[0].group_id
execute store result score @n[tag=mgs.door_new] mgs.zb.door.bgid run data get storage mgs:temp _door_iter[0].back_group_id
execute store result score @n[tag=mgs.door_new] mgs.zb.door.anim run data get storage mgs:temp _door_iter[0].animation

# Store name indexed by link_id
execute store result storage mgs:temp _door_name.id int 1 run data get storage mgs:temp _door_iter[0].link_id
function mgs:v5.0.0/zombies/doors/store_name with storage mgs:temp _door_name

# Register Bookshelf events
execute as @e[tag=mgs.door_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.0/zombies/doors/on_right_click",executor:"source"}
execute as @e[tag=mgs.door_new] run function #bs.interaction:on_hover {run:"function mgs:v5.0.0/zombies/doors/on_hover",executor:"source"}
tag @e[tag=mgs.door_new] remove mgs.door_new

# Continue iteration
data remove storage mgs:temp _door_iter[0]
execute if data storage mgs:temp _door_iter[0] run function mgs:v5.0.0/zombies/doors/setup_iter

