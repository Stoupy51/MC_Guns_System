
#> mgs:v5.1.0/zombies/powerups/activate/nuke
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/admin/powerup_nuke
#			mgs:v5.1.0/zombies/powerups/dispatch_activate
#

execute as @a[tag=mgs.pu_collecting,scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:zombies/bonus/nuke
scoreboard players add @a[scores={mgs.zb.in_game=1}] mgs.zb.points 400
scoreboard players add @a[scores={mgs.zb.in_game=1,mgs.special.double_points=1..}] mgs.zb.points 400

# Kaboom + additional layer + soul whoosh (played together)
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/nuke ambient @s ~ ~ ~ 0.7 1.0
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/nuke_additional ambient @s ~ ~ ~ 0.7 1.0
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/nuke_soul ambient @s ~ ~ ~ 0.8 1.0

# White screen flash for ~1s (blindness fades to white), and set every zombie on fire
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/zombies/powerups/nuke_flash
execute as @e[tag=mgs.nukable] at @s run function mgs:v5.1.0/zombies/powerups/nuke_fire_one

