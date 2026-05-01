
#> mgs:v5.0.0/zombies/powerups/activate/insta_kill
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/dispatch_activate
#

scoreboard players set @a[scores={mgs.zb.in_game=1},gamemode=!spectator] mgs.special.instant_kill 600
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.insta_kill","color":"red","bold":true}]
playsound minecraft:entity.player.levelup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

