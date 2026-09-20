
#> mgs:v5.1.0/zombies/powerups/update_insta_kill_bb
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Find max remaining duration across all players with active insta_kill
scoreboard players set #pu_max_duration mgs.data 0
scoreboard players operation #pu_max_duration mgs.data > @a[scores={mgs.special.instant_kill=1..}] mgs.special.instant_kill

# Steady-off fast path: inactive now AND last tick -> no bossbar command at all
# (the bossbar remove used to run every single tick while the powerup was inactive)
execute if score #pu_max_duration mgs.data matches ..0 if score #pu_prev_insta_kill mgs.data matches ..0 run return 0

# If max duration just hit 0, remove bossbar (once); otherwise update value
execute if score #pu_max_duration mgs.data matches ..0 run bossbar remove mgs:pu_insta_kill
execute if score #pu_max_duration mgs.data matches 1.. store result bossbar mgs:pu_insta_kill value run scoreboard players get #pu_max_duration mgs.data
execute if score #pu_prev_insta_kill mgs.data matches 1.. if score #pu_max_duration mgs.data matches ..0 as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/insta_kill_off ambient @s ~ ~ ~ 0.7 1.0
scoreboard players operation #pu_prev_insta_kill mgs.data = #pu_max_duration mgs.data

