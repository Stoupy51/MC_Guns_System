
#> mgs:v5.1.0/zombies/powerups/update_double_points_bb
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Longest remaining duration across the players who have it.
scoreboard players set #pu_max_duration mgs.data 0
scoreboard players operation #pu_max_duration mgs.data > @a[scores={mgs.special.double_points=1..}] mgs.special.double_points

# Inactive now and last tick: nothing to do.
execute if score #pu_max_duration mgs.data matches ..0 if score #pu_prev_double_points mgs.data matches ..0 run return 0

execute if score #pu_max_duration mgs.data matches ..0 run bossbar remove mgs:pu_double_points
execute if score #pu_max_duration mgs.data matches 1.. store result bossbar mgs:pu_double_points value run scoreboard players get #pu_max_duration mgs.data
execute if score #pu_prev_double_points mgs.data matches 1.. if score #pu_max_duration mgs.data matches ..0 as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/double_points_off ambient @s ~ ~ ~ 0.7 1.0
scoreboard players operation #pu_prev_double_points mgs.data = #pu_max_duration mgs.data

