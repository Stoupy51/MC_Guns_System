
#> mgs:v5.1.0/zombies/powerups/activate/nuke
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/dispatch_activate
#

function mgs:zombies/bonus/nuke
scoreboard players add @a[scores={mgs.zb.in_game=1}] mgs.zb.points 400
scoreboard players add @a[scores={mgs.zb.in_game=1,mgs.special.double_points=1..}] mgs.zb.points 400

execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/nuke ambient @s ~ ~ ~ 0.7 1.0
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/nuke_additional ambient @s ~ ~ ~ 0.7 1.0
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/nuke_soul ambient @s ~ ~ ~ 0.8 1.0

# About 1 s of white flash for every player.
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/zombies/powerups/nuke_flash
execute as @e[tag=mgs.nukable] at @s run function mgs:v5.1.0/zombies/powerups/nuke_fire_one

