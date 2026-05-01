
#> mgs:v5.0.0/zombies/powerups/activate/nuke
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/dispatch_activate
#

execute as @a[tag=mgs.pu_collecting,scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:zombies/bonus/nuke
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.nuke","color":"red","bold":true}]
playsound minecraft:entity.player.levelup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 0.5

