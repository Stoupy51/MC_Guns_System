
#> mgs:v5.1.0/zombies/powerups/activate/max_ammo
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/admin/powerup_max_ammo
#			mgs:v5.1.0/zombies/powerups/dispatch_activate
#

execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:zombies/bonus/max_ammo
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/max_ammo ambient @s ~ ~ ~ 1.0 1.0
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/max_ammo_additional ambient @s ~ ~ ~ 1.0 1.0

