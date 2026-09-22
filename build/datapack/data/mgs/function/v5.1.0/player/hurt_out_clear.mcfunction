
#> mgs:v5.1.0/player/hurt_out_clear
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#			mgs:v5.1.0/player/hurt_rise
#			mgs:v5.1.0/player/hurt_fall
#

execute if score @s mgs.hurt_out matches 1 run posteffect remove @s mgs:hurt_out
execute if score @s mgs.hurt_out matches 2 run posteffect remove @s mgs:hurt_critical_out
scoreboard players reset @s mgs.hurt_out
scoreboard players reset @s mgs.hurt_out_until

