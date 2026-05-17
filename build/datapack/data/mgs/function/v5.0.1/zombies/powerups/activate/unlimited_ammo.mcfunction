
#> mgs:v5.0.1/zombies/powerups/activate/unlimited_ammo
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/dispatch_activate
#

scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.infinite_ammo 600
bossbar remove mgs:pu_unlimited_ammo
bossbar add mgs:pu_unlimited_ammo {"translate":"mgs.unlimited_ammo_30s","bold":true,"color":"green"}
bossbar set mgs:pu_unlimited_ammo max 600
bossbar set mgs:pu_unlimited_ammo value 600
bossbar set mgs:pu_unlimited_ammo color green
bossbar set mgs:pu_unlimited_ammo style progress
bossbar set mgs:pu_unlimited_ammo players @a[scores={mgs.zb.in_game=1}]
playsound minecraft:entity.player.levelup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

