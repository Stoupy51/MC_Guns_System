
#> mgs:v5.4.1/zombies/escort/retarget_lure
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/escort/retarget
#

execute store result storage mgs:temp _escort.x int 1 run data get entity @n[tag=mgs.lure_center] Pos[0]
execute store result storage mgs:temp _escort.y int 1 run data get entity @n[tag=mgs.lure_center] Pos[1]
execute store result storage mgs:temp _escort.z int 1 run data get entity @n[tag=mgs.lure_center] Pos[2]
function mgs:v5.4.1/zombies/escort/set_wander_target with storage mgs:temp _escort

