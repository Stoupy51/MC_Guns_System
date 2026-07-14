
#> mgs:v5.1.0/zombies/horde_ambient_play
#
# @executed	at @e[tag=mgs.zombie_round,distance=..32,sort=random,limit=1]
#
# @within	mgs:v5.1.0/zombies/horde_ambient with storage mgs:temp _horde [ at @e[tag=mgs.zombie_round,distance=..32,sort=random,limit=1] ]
#
# @args		vol (unknown)
#			pitch (unknown)
#

$playsound minecraft:entity.zombie.ambient hostile @s ~ ~ ~ $(vol) $(pitch)

