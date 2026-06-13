
#> mgs:v5.0.1/zombies/powerups/activate/carpenter
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/dispatch_activate
#

function mgs:v5.0.1/zombies/barriers/repair_all
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.carpenter","color":"green","bold":true}]
playsound minecraft:entity.player.levelup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
scoreboard players add @a[scores={mgs.zb.in_game=1}] mgs.zb.points 200

