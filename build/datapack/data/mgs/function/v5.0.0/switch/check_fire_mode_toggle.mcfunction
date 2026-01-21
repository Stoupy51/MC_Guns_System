
#> mgs:v5.0.0/switch/check_fire_mode_toggle
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Check if player dropped a weapon
execute if score @s mgs.dropped matches 1.. run function mgs:v5.0.0/switch/toggle_fire_mode
scoreboard players reset @s mgs.dropped

