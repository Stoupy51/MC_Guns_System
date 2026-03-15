
#> mgs:v5.0.0/zombies/doors/open_one
#
# @executed	as @e[tag=mgs.door] & at @s
#
# @within	mgs:v5.0.0/zombies/doors/on_right_click [ as @e[tag=mgs.door] & at @s ]
#

# Use stored rotation and side-aware local offset so both front/back interactions
# target the same door block position.
execute store result storage mgs:temp _door_open.rot int 1 run scoreboard players get @s mgs.zb.door.rot
data modify storage mgs:temp _door_open.offset set value -0.75
execute if entity @s[tag=mgs.door_back] run data modify storage mgs:temp _door_open.offset set value 0.75

# Remove block based on animation type (0 = destroy with particles, 1+ = silent air)
execute if score @s mgs.zb.door.anim matches 0 run function mgs:v5.0.0/zombies/doors/remove_block_destroy with storage mgs:temp _door_open
execute unless score @s mgs.zb.door.anim matches 0 run function mgs:v5.0.0/zombies/doors/remove_block_silent with storage mgs:temp _door_open

# Unlock primary group
execute store result storage mgs:temp _door_unlock.gid int 1 run scoreboard players get @s mgs.zb.door.gid
function mgs:v5.0.0/zombies/doors/unlock_group with storage mgs:temp _door_unlock

# Unlock back group if applicable (back_group_id != -1)
execute unless score @s mgs.zb.door.bgid matches -1 run function mgs:v5.0.0/zombies/doors/unlock_back_group

# Kill door interaction entity
kill @s

