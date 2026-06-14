
#> mgs:v5.0.1/zombies/powerups/activate/max_ammo
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/dispatch_activate
#

execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:zombies/bonus/max_ammo
playsound mgs:zombies/powerups/max_ammo ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
playsound mgs:zombies/powerups/max_ammo_additional ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

