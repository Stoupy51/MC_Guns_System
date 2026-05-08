
#> mgs:v5.0.1/missions/prep_tick
#
# @within	mgs:v5.0.1/tick
#

# Detect class changes during prep
execute as @a[scores={mgs.mi.in_game=1}] unless score @s mgs.mp.prev_class = @s mgs.mp.class at @s run function mgs:v5.0.1/multiplayer/apply_class
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.mp.prev_class = @s mgs.mp.class

