
#> mgs:v5.1.0/zombies/vocals/attack
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/hurt_player/on_hurt
#

scoreboard players operation @s mgs.zb.vox_attack = #total_tick mgs.data
scoreboard players add @s mgs.zb.vox_attack 20
execute at @n[tag=mgs.zombie_round,tag=!mgs.zb_dog,distance=..3.5] run playsound mgs:zombies/entity/attack hostile @s ~ ~ ~ 1.0 1.0

