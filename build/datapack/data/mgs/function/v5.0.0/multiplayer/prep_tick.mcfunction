
#> mgs:v5.0.0/multiplayer/prep_tick
#
# @within	mgs:v5.0.0/tick
#

# Check for class changes and apply immediately
execute as @a[scores={mgs.mp.in_game=1}] unless score @s mgs.mp.class = @s mgs.mp.prev_class unless score @s mgs.mp.class matches 0 at @s run function mgs:v5.0.0/multiplayer/apply_class
execute as @a[scores={mgs.mp.in_game=1}] run scoreboard players operation @s mgs.mp.prev_class = @s mgs.mp.class

