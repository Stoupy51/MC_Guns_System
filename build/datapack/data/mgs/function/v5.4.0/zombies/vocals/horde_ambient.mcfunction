
#> mgs:v5.4.0/zombies/vocals/horde_ambient
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/horde_ambient with storage mgs:temp _horde [ at @e[type=minecraft:zombie,tag=mgs.zombie_round,distance=..32,sort=random,limit=1] ]
#
# @args		vol (unknown)
#			pitch (unknown)
#

$playsound mgs:zombies/entity/ambient hostile @s ~ ~ ~ $(vol) $(pitch)

