
#> mgs:v5.0.0/zombies/barriers/destroyed_tick
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/tick
#

# @s = destroyed barrier display, at @s
execute store result score #barrier_id mgs.data run scoreboard players get @s mgs.zb.barrier.id
execute store result storage mgs:temp _brptick.radius int 1 run scoreboard players get @s mgs.zb.barrier.radius

# Handle repair timer or find a new repairer (both macros using radius)
execute if score @s mgs.zb.barrier.rp_timer matches 1.. run function mgs:v5.0.0/zombies/barriers/handle_repair with storage mgs:temp _brptick
execute if score @s mgs.zb.barrier.rp_timer matches 0 if score @s mgs.zb.barrier.state matches 1 run function mgs:v5.0.0/zombies/barriers/find_repairer with storage mgs:temp _brptick

