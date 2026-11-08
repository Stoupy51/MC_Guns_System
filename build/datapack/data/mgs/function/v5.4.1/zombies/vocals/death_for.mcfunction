
#> mgs:v5.4.1/zombies/vocals/death_for
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/vocals/death [ as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] ]
#

scoreboard players operation @s mgs.zb.vox_death = #total_tick mgs.data
scoreboard players add @s mgs.zb.vox_death 10
playsound mgs:zombies/entity/death hostile @s ~ ~ ~ 2.0 1.0

