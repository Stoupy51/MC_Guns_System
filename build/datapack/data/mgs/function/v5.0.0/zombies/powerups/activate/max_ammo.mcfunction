
#> mgs:v5.0.0/zombies/powerups/activate/max_ammo
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/dispatch_activate
#

execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:zombies/bonus/max_ammo
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.max_ammo","color":"aqua","bold":true}]
playsound minecraft:entity.player.levelup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

