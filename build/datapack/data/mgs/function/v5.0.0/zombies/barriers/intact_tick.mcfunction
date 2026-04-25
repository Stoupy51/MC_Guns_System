
#> mgs:v5.0.0/zombies/barriers/intact_tick
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/tick
#

# @s = intact barrier display, at @s
execute store result score #barrier_id mgs.data run scoreboard players get @s mgs.zb.barrier.id
execute store result storage mgs:temp _btick.radius int 1 run scoreboard players get @s mgs.zb.barrier.radius

# Freeze all zombies in radius (macro)
function mgs:v5.0.0/zombies/barriers/freeze_zombies with storage mgs:temp _btick

# Handle remove timer or find a new remover (both macros using radius)
execute if score @s mgs.zb.barrier.r_timer matches 1.. run function mgs:v5.0.0/zombies/barriers/handle_removing with storage mgs:temp _btick
execute if score @s mgs.zb.barrier.r_timer matches 0 if score @s mgs.zb.barrier.state matches 0 run function mgs:v5.0.0/zombies/barriers/find_remover with storage mgs:temp _btick

