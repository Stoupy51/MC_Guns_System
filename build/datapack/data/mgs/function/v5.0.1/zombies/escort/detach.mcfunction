
#> mgs:v5.0.1/zombies/escort/detach
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.0.1/zombies/escort/zombie_tick
#			mgs:v5.0.1/zombies/escort/release
#			mgs:v5.0.1/zombies/escort/give_up
#

tag @s remove mgs.zb_escorted
data modify entity @s NoAI set value 0b
scoreboard players remove #zb_escort_count mgs.data 1

# Fresh stuck-tracking window from wherever the escort left the zombie
scoreboard players set @s mgs.zb.stuck_dist 4
execute store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

