
#> mgs:v5.0.0/player/config/process
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# 1 = Show config menu
# 2 = Toggle hitmarker sound
# 3 = Toggle damage debug in chat
execute if score @s mgs.player.config matches 1 run function mgs:v5.0.0/player/config/menu
execute if score @s mgs.player.config matches 2 run function mgs:v5.0.0/player/config/toggle_hitmarker
execute if score @s mgs.player.config matches 3 run function mgs:v5.0.0/player/config/toggle_damage_debug

# Reset score
scoreboard players set @s mgs.player.config 0

