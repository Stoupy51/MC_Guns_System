
#> mgs:v5.0.1/switch/check_reload_on_drop
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/tick
#

# Check if player dropped a weapon
execute if score @s mgs.dropped matches 1.. run function mgs:v5.0.1/switch/reload_to_dropped_weapon
scoreboard players reset @s mgs.dropped

