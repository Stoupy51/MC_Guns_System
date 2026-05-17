
#> mgs:v5.0.1/zombies/powerups/activate/double_points
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/dispatch_activate
#

scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.double_points 600
bossbar remove mgs:pu_double_points
bossbar create mgs:pu_double_points {"translate":"mgs.double_points_30s","bold":true,"color":"gold"}
bossbar set mgs:pu_double_points max 600
bossbar set mgs:pu_double_points value 600
bossbar set mgs:pu_double_points color gold
bossbar set mgs:pu_double_points style progress
bossbar set mgs:pu_double_points players @a[scores={mgs.zb.in_game=1}]
playsound minecraft:entity.player.levelup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

