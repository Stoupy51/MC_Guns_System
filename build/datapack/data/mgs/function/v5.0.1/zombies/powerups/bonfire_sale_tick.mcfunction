
#> mgs:v5.0.1/zombies/powerups/bonfire_sale_tick
#
# @within	mgs:v5.0.1/zombies/game_tick
#

scoreboard players remove #zb_bonfire_sale_timer mgs.data 1
execute if score #zb_bonfire_sale_timer mgs.data matches ..0 run bossbar remove mgs:pu_bonfire_sale
execute if score #zb_bonfire_sale_timer mgs.data matches 1.. store result bossbar mgs:pu_bonfire_sale value run scoreboard players get #zb_bonfire_sale_timer mgs.data

