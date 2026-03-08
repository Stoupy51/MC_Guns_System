
#> mgs:v5.0.0/zombies/doors/unlock_back_group
#
# @executed	as @e[tag=mgs.door] & at @s
#
# @within	mgs:v5.0.0/zombies/doors/open_one
#

execute store result storage mgs:temp _door_unlock.gid int 1 run scoreboard players get @s mgs.zb.door.bgid
function mgs:v5.0.0/zombies/doors/unlock_group with storage mgs:temp _door_unlock

