
#> mgs:v5.4.3/switch/check_fire_mode_on_drop
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.4.3/player/tick
#			mgs:v5.4.3/dialog/close_then
#

execute if score @s mgs.dropped matches 1.. run function mgs:v5.4.3/switch/fire_mode_on_dropped_weapon
scoreboard players reset @s mgs.dropped

