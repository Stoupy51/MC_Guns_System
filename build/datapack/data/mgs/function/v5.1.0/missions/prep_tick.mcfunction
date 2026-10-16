
#> mgs:v5.1.0/missions/prep_tick
#
# @within	mgs:v5.1.0/tick
#

execute unless score #in_missions_map mgs.data matches 1 run return run function mgs:v5.1.0/shared/enter_map {mode:"missions",fn:"mgs:v5.1.0/missions/prep_tick"}

execute as @a[scores={mgs.mi.in_game=1}] unless score @s mgs.mp.prev_class = @s mgs.mp.class at @s run function mgs:v5.1.0/multiplayer/apply_class
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.mp.prev_class = @s mgs.mp.class

