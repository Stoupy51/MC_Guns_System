
#> mgs:v5.1.0/zombies/powerups/activate/fire_sale
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/admin/powerup
#			mgs:v5.1.0/zombies/powerups/dispatch_activate
#

# An already running Fire Sale does not restart its song or temporary boxes.
scoreboard players set #fs_was_active mgs.data 0
execute if score #zb_fire_sale_timer mgs.data matches 1.. run scoreboard players set #fs_was_active mgs.data 1

# Saved only outside a Fire Sale, so the discount is never snapshotted.
execute if score #zb_fire_sale_timer mgs.data matches ..0 run scoreboard players operation #zb_fire_sale_saved mgs.data = #zb_mystery_box_price mgs.config

scoreboard players set #zb_mystery_box_price mgs.config 10
scoreboard players set #zb_fire_sale_timer mgs.data 600

bossbar remove mgs:pu_fire_sale
bossbar add mgs:pu_fire_sale {"translate":"mgs.fire_sale","bold":true,"color":"light_purple"}
bossbar set mgs:pu_fire_sale max 600
bossbar set mgs:pu_fire_sale value 600
bossbar set mgs:pu_fire_sale color pink
bossbar set mgs:pu_fire_sale style progress
bossbar set mgs:pu_fire_sale players @a[scores={mgs.zb.in_game=1}]

execute if score #fs_was_active mgs.data matches 0 run execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/fire_sale ambient @s ~ ~ ~ 0.7 1.0
execute if score #fs_was_active mgs.data matches 0 as @a[scores={mgs.zb.in_game=1}] run playsound mgs:zombies/powerups/fire_sale_song ambient @s ~ ~ ~ 0.3 1.0
execute if score #fs_was_active mgs.data matches 0 run function mgs:v5.1.0/zombies/mystery_box/fire_sale_start

