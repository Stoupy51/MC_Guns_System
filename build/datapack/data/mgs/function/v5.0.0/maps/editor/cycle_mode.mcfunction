
#> mgs:v5.0.0/maps/editor/cycle_mode
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/maps/editor/tick
#

# Advance display mode
scoreboard players add @s mgs.mp.map_disp 1
execute if score @s mgs.mp.map_disp matches 3.. run scoreboard players set @s mgs.mp.map_disp 0

# Clear inventory and re-give tools for new mode
clear @s
function mgs:v5.0.0/maps/editor/give_tools

# Announce
execute if score @s mgs.mp.map_disp matches 0 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.switched_to_multiplayer_mode","color":"gold"}]
execute if score @s mgs.mp.map_disp matches 1 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.switched_to_zombies_mode","color":"dark_green"}]
execute if score @s mgs.mp.map_disp matches 2 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.switched_to_missions_mode","color":"aqua"}]

