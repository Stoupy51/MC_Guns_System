
#> mgs:v5.4.1/zombies/powerups/activate/carpenter
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/admin/powerup
#			mgs:v5.4.1/zombies/powerups/dispatch_activate
#

function mgs:v5.4.1/zombies/barricades/repair_all
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/carpenter ambient @s ~ ~ ~ 0.7 1.0
scoreboard players add @a[scores={mgs.zb.in_game=1}] mgs.zb.points 200
scoreboard players add @a[scores={mgs.zb.in_game=1,mgs.special.double_points=1..}] mgs.zb.points 200

