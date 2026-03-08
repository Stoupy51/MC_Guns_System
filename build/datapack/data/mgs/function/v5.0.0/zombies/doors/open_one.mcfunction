
#> mgs:v5.0.0/zombies/doors/open_one
#
# @executed	as @e[tag=mgs.door] & at @s
#
# @within	mgs:v5.0.0/zombies/doors/on_right_click [ as @e[tag=mgs.door] & at @s ]
#

# Remove block based on animation type (0 = destroy with particles, 1+ = silent air)
execute if score @s mgs.zb.door.anim matches 0 run setblock ~ ~ ~ air destroy
execute if score @s mgs.zb.door.anim matches 0 run kill @e[type=item,distance=..1.5]
execute unless score @s mgs.zb.door.anim matches 0 run setblock ~ ~ ~ air

# Unlock primary group
execute store result storage mgs:temp _door_unlock.gid int 1 run scoreboard players get @s mgs.zb.door.gid
function mgs:v5.0.0/zombies/doors/unlock_group with storage mgs:temp _door_unlock

# Unlock back group if applicable (back_group_id != -1)
execute unless score @s mgs.zb.door.bgid matches -1 run function mgs:v5.0.0/zombies/doors/unlock_back_group

# Kill door interaction entity
kill @s

