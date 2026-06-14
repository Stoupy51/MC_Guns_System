
#> mgs:v5.0.1/zombies/powerups/activate/bonfire_sale
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/dispatch_activate
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
playsound mgs:zombies/powerups/bonfire_sale ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

