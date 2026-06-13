
#> mgs:v5.0.1/zombies/powerups/fire_sale_tick
#
# @within	mgs:v5.0.1/zombies/game_tick
#

# Decrement the shared timer
scoreboard players remove #zb_fire_sale_timer mgs.data 1

# Expired: restore the saved price and remove the bossbar
execute if score #zb_fire_sale_timer mgs.data matches ..0 run scoreboard players operation #zb_mystery_box_price mgs.config = #zb_fire_sale_saved mgs.data
execute if score #zb_fire_sale_timer mgs.data matches ..0 run bossbar remove mgs:pu_fire_sale

# Still active: update bossbar value + countdown label
execute if score #zb_fire_sale_timer mgs.data matches 1.. store result bossbar mgs:pu_fire_sale value run scoreboard players get #zb_fire_sale_timer mgs.data
execute if score #zb_fire_sale_timer mgs.data matches 1.. run scoreboard players operation #zb_fs_seconds mgs.data = #zb_fire_sale_timer mgs.data
execute if score #zb_fire_sale_timer mgs.data matches 1.. run scoreboard players operation #zb_fs_seconds mgs.data /= #20 mgs.data
execute if score #zb_fire_sale_timer mgs.data matches 1.. run bossbar set mgs:pu_fire_sale name [[{"translate":"mgs.fire_sale_2","color":"light_purple","bold":true}, " - "],{"score":{"name":"#zb_fs_seconds","objective":"mgs.data"},"color":"light_purple"},"s"]

