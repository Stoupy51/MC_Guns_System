
#> mgs:v5.3.0/zombies/vocals/horde_sprint
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/horde_ambient with storage mgs:temp _horde [ at @n[type=minecraft:zombie,tag=...,distance=..32,sort=random] ]
#
# @args		vol (unknown)
#

$playsound mgs:zombies/entity/sprint hostile @s ~ ~ ~ $(vol) 1.0
return 1

