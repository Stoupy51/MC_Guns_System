
#> mgs:v5.0.1/zombies/powerups/activate/carpenter
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/dispatch_activate
#

function mgs:v5.0.1/zombies/barriers/repair_all
playsound mgs:zombies/powerups/carpenter ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
scoreboard players add @a[scores={mgs.zb.in_game=1}] mgs.zb.points 200
scoreboard players add @a[scores={mgs.zb.in_game=1,mgs.special.double_points=1..}] mgs.zb.points 200

