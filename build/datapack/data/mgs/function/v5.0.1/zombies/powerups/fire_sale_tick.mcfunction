
#> mgs:v5.0.1/zombies/powerups/fire_sale_tick
#
# @within	mgs:v5.0.1/zombies/game_tick
#

# Decrement the shared timer
scoreboard players remove #zb_fire_sale_timer mgs.data 1

# Expired: restore the saved price, remove the bossbar, stop the song, remove temp boxes
execute if score #zb_fire_sale_timer mgs.data matches ..0 run scoreboard players operation #zb_mystery_box_price mgs.config = #zb_fire_sale_saved mgs.data
execute if score #zb_fire_sale_timer mgs.data matches ..0 run bossbar remove mgs:pu_fire_sale
execute if score #zb_fire_sale_timer mgs.data matches ..0 run stopsound @a[scores={mgs.zb.in_game=1}] ambient mgs:zombies/powerups/fire_sale_song
execute if score #zb_fire_sale_timer mgs.data matches ..0 run function mgs:v5.0.1/zombies/mystery_box/fire_sale_end

# Still active: update bossbar value
execute if score #zb_fire_sale_timer mgs.data matches 1.. store result bossbar mgs:pu_fire_sale value run scoreboard players get #zb_fire_sale_timer mgs.data

