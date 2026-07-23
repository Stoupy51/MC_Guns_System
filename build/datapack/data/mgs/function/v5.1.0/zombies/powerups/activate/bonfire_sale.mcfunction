
#> mgs:v5.1.0/zombies/powerups/activate/bonfire_sale
#
# @within	mgs:v5.1.0/zombies/admin/powerup_bonfire_sale
#			mgs:v5.1.0/zombies/powerups/dispatch_activate
#

scoreboard players set #zb_bonfire_sale_timer mgs.data 600

# Bossbar
bossbar remove mgs:pu_bonfire_sale
bossbar add mgs:pu_bonfire_sale {"translate":"mgs.bonfire_sale","bold":true,"color":"gold"}
bossbar set mgs:pu_bonfire_sale max 600
bossbar set mgs:pu_bonfire_sale value 600
bossbar set mgs:pu_bonfire_sale color yellow
bossbar set mgs:pu_bonfire_sale style progress
bossbar set mgs:pu_bonfire_sale players @a[scores={mgs.zb.in_game=1}]
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/bonfire_sale ambient @s ~ ~ ~ 0.7 1.0

