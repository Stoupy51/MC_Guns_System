
#> mgs:v5.4.2/zombies/doors/unlock_back_group
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/doors/open_one
#

execute store result storage mgs:temp _door_unlock.gid int 1 run scoreboard players get @s mgs.zb.door.bgid
function mgs:v5.4.2/zombies/doors/unlock_group with storage mgs:temp _door_unlock

