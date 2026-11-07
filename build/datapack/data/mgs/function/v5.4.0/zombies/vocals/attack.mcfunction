
#> mgs:v5.4.0/zombies/vocals/attack
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/hurt_player/on_hurt
#

scoreboard players operation @s mgs.zb.vox_attack = #total_tick mgs.data
scoreboard players add @s mgs.zb.vox_attack 20
execute at @n[type=minecraft:zombie,tag=mgs.zombie_round,distance=..3.5] run playsound mgs:zombies/entity/attack hostile @s ~ ~ ~ 1.0 1.0

