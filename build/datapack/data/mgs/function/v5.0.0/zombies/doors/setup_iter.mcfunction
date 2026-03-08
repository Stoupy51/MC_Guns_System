
#> mgs:v5.0.0/zombies/doors/setup_iter
#
# @within	mgs:v5.0.0/zombies/doors/setup
#			mgs:v5.0.0/zombies/doors/setup_iter
#

# Read relative position and convert to absolute
execute store result score #_dx mgs.data run data get storage mgs:temp _door_iter[0].pos[0]
execute store result score #_dy mgs.data run data get storage mgs:temp _door_iter[0].pos[1]
execute store result score #_dz mgs.data run data get storage mgs:temp _door_iter[0].pos[2]
scoreboard players operation #_dx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_dy mgs.data += #gm_base_y mgs.data
scoreboard players operation #_dz mgs.data += #gm_base_z mgs.data

# Store absolute position and block for macro
execute store result storage mgs:temp _door.x int 1 run scoreboard players get #_dx mgs.data
execute store result storage mgs:temp _door.y int 1 run scoreboard players get #_dy mgs.data
execute store result storage mgs:temp _door.z int 1 run scoreboard players get #_dz mgs.data
data modify storage mgs:temp _door.block set from storage mgs:temp _door_iter[0].block

# Place block and summon interaction entity
function mgs:v5.0.0/zombies/doors/place_at with storage mgs:temp _door

# Set scoreboards on newly spawned door entity
execute store result score @n[tag=_door_new] mgs.zb.door.link run data get storage mgs:temp _door_iter[0].link_id
execute store result score @n[tag=_door_new] mgs.zb.door.price run data get storage mgs:temp _door_iter[0].price
execute store result score @n[tag=_door_new] mgs.zb.door.gid run data get storage mgs:temp _door_iter[0].group_id
execute store result score @n[tag=_door_new] mgs.zb.door.bgid run data get storage mgs:temp _door_iter[0].back_group_id
execute store result score @n[tag=_door_new] mgs.zb.door.anim run data get storage mgs:temp _door_iter[0].animation

# Register Bookshelf events
execute as @e[tag=_door_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.0/zombies/doors/on_right_click",executor:"source"}
execute as @e[tag=_door_new] run function #bs.interaction:on_hover_enter {run:"function mgs:v5.0.0/zombies/doors/on_hover_enter",executor:"source"}
execute as @e[tag=_door_new] run function #bs.interaction:on_hover_leave {run:"function mgs:v5.0.0/zombies/doors/on_hover_leave",executor:"source"}
tag @e[tag=_door_new] remove _door_new

# Continue iteration
data remove storage mgs:temp _door_iter[0]
execute if data storage mgs:temp _door_iter[0] run function mgs:v5.0.0/zombies/doors/setup_iter

