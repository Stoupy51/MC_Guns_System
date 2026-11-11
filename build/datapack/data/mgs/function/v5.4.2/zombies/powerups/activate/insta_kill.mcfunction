
#> mgs:v5.4.2/zombies/powerups/activate/insta_kill
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/admin/powerup
#			mgs:v5.4.2/zombies/powerups/dispatch_activate
#

scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.instant_kill 600
bossbar remove mgs:pu_insta_kill
bossbar add mgs:pu_insta_kill {"translate":"mgs.insta_kill","fallback":"Insta Kill","bold":true,"color":"red"}
bossbar set mgs:pu_insta_kill max 600
bossbar set mgs:pu_insta_kill value 600
bossbar set mgs:pu_insta_kill color red
bossbar set mgs:pu_insta_kill style progress
bossbar set mgs:pu_insta_kill players @a[scores={mgs.zb.in_game=1}]
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/insta_kill ambient @s ~ ~ ~ 1.0 1.0

