
#> mgs:v5.0.1/zombies/powerups/update_double_points_bb
#
# @within	mgs:v5.0.1/zombies/game_tick
#

# Find max remaining duration across all players with active double_points
scoreboard players set #pu_max_duration mgs.data 0
scoreboard players operation #pu_max_duration mgs.data > @a[scores={mgs.special.double_points=1..}] mgs.special.double_points

# If max duration is 0, remove bossbar; otherwise update value
execute if score #pu_max_duration mgs.data matches ..0 run bossbar remove mgs:pu_double_points
execute if score #pu_max_duration mgs.data matches 1.. store result bossbar mgs:pu_double_points value run scoreboard players get #pu_max_duration mgs.data
execute if score #pu_prev_double_points mgs.data matches 1.. if score #pu_max_duration mgs.data matches ..0 as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/double_points_off ambient @s ~ ~ ~ 1.0 1.0
scoreboard players operation #pu_prev_double_points mgs.data = #pu_max_duration mgs.data

