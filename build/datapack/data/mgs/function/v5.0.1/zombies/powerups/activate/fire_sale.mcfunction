
#> mgs:v5.0.1/zombies/powerups/activate/fire_sale
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/dispatch_activate
#

# Save the normal price only when no Fire Sale is already running (so we don't snapshot the discount)
execute if score #zb_fire_sale_timer mgs.data matches ..0 run scoreboard players operation #zb_fire_sale_saved mgs.data = #zb_mystery_box_price mgs.config

# Apply the discount and (re)start the timer
scoreboard players set #zb_mystery_box_price mgs.config 10
scoreboard players set #zb_fire_sale_timer mgs.data 600

# Bossbar
bossbar remove mgs:pu_fire_sale
bossbar add mgs:pu_fire_sale {"translate":"mgs.fire_sale_30s","bold":true,"color":"light_purple"}
bossbar set mgs:pu_fire_sale max 600
bossbar set mgs:pu_fire_sale value 600
bossbar set mgs:pu_fire_sale color pink
bossbar set mgs:pu_fire_sale style progress
bossbar set mgs:pu_fire_sale players @a[scores={mgs.zb.in_game=1}]

tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.fire_sale","color":"light_purple","bold":true},{"translate":"mgs.mystery_box_costs_10_points","color":"white"}]
playsound minecraft:entity.player.levelup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

