
#> mgs:v5.0.0/zombies/barriers/start_removing_zombie
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/find_remover
#

# @s = zombie assigned as remover
tag @s add mgs.barrier_removing
scoreboard players operation @s mgs.zb.barrier.removing_id = #barrier_id mgs.data
scoreboard players set #barrier_found_remover mgs.data 1

