
#> mgs:v5.0.1/zombies/powerups/update_insta_kill_bb
#
# @within	mgs:v5.0.1/zombies/game_tick
#

# Find max remaining duration across all players with active insta_kill
scoreboard players set #pu_max_duration mgs.data 0
scoreboard players operation #pu_max_duration mgs.data > @a[scores={mgs.special.instant_kill=1..}] mgs.special.instant_kill

# If max duration is 0, remove bossbar; otherwise update value
execute if score #pu_max_duration mgs.data matches ..0 run bossbar remove mgs:pu_insta_kill
execute if score #pu_max_duration mgs.data matches 1.. store result bossbar mgs:pu_insta_kill value run scoreboard players get #pu_max_duration mgs.data
execute if score #pu_prev_insta_kill mgs.data matches 1.. if score #pu_max_duration mgs.data matches ..0 as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/insta_kill_off ambient @s ~ ~ ~ 0.7 1.0
scoreboard players operation #pu_prev_insta_kill mgs.data = #pu_max_duration mgs.data

