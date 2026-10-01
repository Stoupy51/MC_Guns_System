
#> mgs:v5.1.0/player/hurt_sweep
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/hurt_tick
#

# @s = a player whose scores say no overlay is applied
posteffect remove @s mgs:hurt_0_1
posteffect remove @s mgs:hurt_0_2
posteffect remove @s mgs:hurt_1_0
posteffect remove @s mgs:hurt_1_1
posteffect remove @s mgs:hurt_1_2
posteffect remove @s mgs:hurt_2_0
posteffect remove @s mgs:hurt_2_1
posteffect remove @s mgs:hurt_2_2

