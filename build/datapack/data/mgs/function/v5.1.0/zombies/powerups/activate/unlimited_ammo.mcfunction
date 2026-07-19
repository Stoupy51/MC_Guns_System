
#> mgs:v5.1.0/zombies/powerups/activate/unlimited_ammo
#
# @within	mgs:v5.1.0/zombies/admin/powerup_unlimited_ammo
#			mgs:v5.1.0/zombies/powerups/dispatch_activate
#

scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.infinite_ammo 600
bossbar remove mgs:pu_unlimited_ammo
bossbar add mgs:pu_unlimited_ammo {"translate":"mgs.unlimited_ammo","bold":true,"color":"green"}
bossbar set mgs:pu_unlimited_ammo max 600
bossbar set mgs:pu_unlimited_ammo value 600
bossbar set mgs:pu_unlimited_ammo color green
bossbar set mgs:pu_unlimited_ammo style progress
bossbar set mgs:pu_unlimited_ammo players @a[scores={mgs.zb.in_game=1}]
playsound minecraft:entity.player.levelup ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

