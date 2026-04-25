
#> mgs:v5.0.0/zombies/barriers/start_repairing_player
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/find_repairer
#

# @s = player assigned as repairer
tag @s add mgs.barrier_repairing
scoreboard players operation @s mgs.zb.barrier.repairing_id = #barrier_id mgs.data
scoreboard players set #barrier_found_repairer mgs.data 1

