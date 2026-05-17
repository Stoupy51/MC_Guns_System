
#> mgs:v5.0.1/zombies/powerups/update_unlimited_ammo_bb
#
# @within	mgs:v5.0.1/zombies/game_tick
#

# Find max remaining duration across all players with active unlimited_ammo
scoreboard players set #pu_max_duration mgs.data 0
scoreboard players operation #pu_max_duration mgs.data > @a[scores={mgs.special.infinite_ammo=1..}] mgs.special.infinite_ammo

# If max duration is 0, remove bossbar; otherwise update value and name with countdown
execute if score #pu_max_duration mgs.data matches ..0 run bossbar remove mgs:pu_unlimited_ammo
execute if score #pu_max_duration mgs.data matches 1.. store result bossbar mgs:pu_unlimited_ammo value run scoreboard players get #pu_max_duration mgs.data
execute if score #pu_max_duration mgs.data matches 1.. run scoreboard players operation #pu_seconds mgs.data = #pu_max_duration mgs.data
execute if score #pu_max_duration mgs.data matches 1.. run scoreboard players operation #pu_seconds mgs.data /= #20 mgs.data
execute if score #pu_max_duration mgs.data matches 1.. run bossbar set mgs:pu_unlimited_ammo name [[{"translate":"mgs.unlimited_ammo","color":"green","bold":true}, " - "],{"score":{"name":"#pu_seconds","objective":"mgs.data"},"color":"green"},"s"]

