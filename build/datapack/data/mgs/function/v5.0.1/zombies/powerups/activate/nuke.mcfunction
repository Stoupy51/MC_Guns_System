
#> mgs:v5.0.1/zombies/powerups/activate/nuke
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/dispatch_activate
#

execute as @a[tag=mgs.pu_collecting,scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:zombies/bonus/nuke
scoreboard players add @a[scores={mgs.zb.in_game=1}] mgs.zb.points 400
scoreboard players add @a[scores={mgs.zb.in_game=1,mgs.special.double_points=1..}] mgs.zb.points 400

# Kaboom + additional layer + soul whoosh (played together)
playsound mgs:zombies/powerups/nuke ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
playsound mgs:zombies/powerups/nuke_additional ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
playsound mgs:zombies/powerups/nuke_soul ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.8 1.0

# White screen flash for ~1s (blindness fades to white), and set every zombie on fire
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.0.1/zombies/powerups/nuke_flash
execute as @e[tag=mgs.nukable] at @s run function mgs:v5.0.1/zombies/powerups/nuke_fire_one

