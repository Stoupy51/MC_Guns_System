
#> mgs:v5.0.1/zombies/powerups/activate/insta_kill
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/dispatch_activate
#

scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.instant_kill 600
bossbar remove mgs:pu_insta_kill
bossbar create mgs:pu_insta_kill {"translate":"mgs.insta_kill_30s","bold":true,"color":"red"}
bossbar set mgs:pu_insta_kill max 600
bossbar set mgs:pu_insta_kill value 600
bossbar set mgs:pu_insta_kill color red
bossbar set mgs:pu_insta_kill style progress
bossbar set mgs:pu_insta_kill players @a[scores={mgs.zb.in_game=1}]
playsound minecraft:entity.player.levelup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

