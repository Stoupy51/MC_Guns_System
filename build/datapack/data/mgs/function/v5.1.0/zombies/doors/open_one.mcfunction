
#> mgs:v5.1.0/zombies/doors/open_one
#
# @executed	as @e[tag=mgs.door] & at @s
#
# @within	mgs:v5.1.0/zombies/doors/on_right_click [ as @e[tag=mgs.door] & at @s ]
#

# Stored rotation and side-aware offset, so both interactions target the same door block.
execute store result storage mgs:temp _door_open.rot int 1 run scoreboard players get @s mgs.zb.door.rot
data modify storage mgs:temp _door_open.offset set value -0.75
execute if entity @s[tag=mgs.door_back] run data modify storage mgs:temp _door_open.offset set value 0.75

# anim 0 breaks the block with particles, 1+ sets air silently.
execute if score @s mgs.zb.door.anim matches 0 run function mgs:v5.1.0/zombies/doors/remove_block_destroy with storage mgs:temp _door_open
execute unless score @s mgs.zb.door.anim matches 0 run function mgs:v5.1.0/zombies/doors/remove_block_silent with storage mgs:temp _door_open

# link_id is the front room's group_id.
execute store result storage mgs:temp _door_unlock.gid int 1 run scoreboard players get @s mgs.zb.door.link
function mgs:v5.1.0/zombies/doors/unlock_group with storage mgs:temp _door_unlock

# back_group_id -1 means no back room.
execute unless score @s mgs.zb.door.bgid matches -1 run function mgs:v5.1.0/zombies/doors/unlock_back_group

kill @s

