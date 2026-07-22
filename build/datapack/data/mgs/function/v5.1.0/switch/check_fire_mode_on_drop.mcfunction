
#> mgs:v5.1.0/switch/check_fire_mode_on_drop
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# Check if player dropped a weapon
execute if score @s mgs.dropped matches 1.. run function mgs:v5.1.0/switch/fire_mode_on_dropped_weapon
scoreboard players reset @s mgs.dropped

