
#> mgs:v5.0.0/zombies/on_kill_signal
#
# @within	#mgs:signals/on_kill
#

# Only process if zombies game is active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Award kill points (with passive bonus if applicable)
scoreboard players operation @s mgs.zb.points += #zb_points_kill mgs.config

# Apply x1.2 points passive: add 20% extra
execute if score @s mgs.zb.passive matches 1 run scoreboard players operation #additional mgs.data = #zb_points_kill mgs.config
execute if score @s mgs.zb.passive matches 1 run scoreboard players operation #additional mgs.data /= #5 mgs.data
execute if score @s mgs.zb.passive matches 1 run scoreboard players operation @s mgs.zb.points += #additional mgs.data

scoreboard players add @s mgs.zb.kills 1

