
#> mgs:v5.1.0/zombies/powerups/update_unlimited_ammo_bb
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Find max remaining duration across all players with active unlimited_ammo
scoreboard players set #pu_max_duration mgs.data 0
scoreboard players operation #pu_max_duration mgs.data > @a[scores={mgs.special.infinite_ammo=1..}] mgs.special.infinite_ammo

# Steady-off fast path: inactive now AND last tick -> no bossbar command at all
# (the bossbar remove used to run every single tick while the powerup was inactive)
execute if score #pu_max_duration mgs.data matches ..0 if score #pu_prev_unlimited_ammo mgs.data matches ..0 run return 0

# If max duration just hit 0, remove bossbar (once); otherwise update value
execute if score #pu_max_duration mgs.data matches ..0 run bossbar remove mgs:pu_unlimited_ammo
execute if score #pu_max_duration mgs.data matches 1.. store result bossbar mgs:pu_unlimited_ammo value run scoreboard players get #pu_max_duration mgs.data
scoreboard players operation #pu_prev_unlimited_ammo mgs.data = #pu_max_duration mgs.data

