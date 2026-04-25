
#> mgs:v5.0.0/zombies/barriers/handle_removing
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/intact_tick with storage mgs:temp _btick
#
# @args		radius (unknown)
#

# MACRO: @s = intact barrier marker, $(radius) = sphere radius
# Verify assigned remover is still in range and matches this barrier
scoreboard players set #barrier_remover_valid mgs.data 0
$execute as @e[tag=mgs.barrier_removing,distance=..$(radius)] at @s if score @s mgs.zb.barrier.removing_id = #barrier_id mgs.data run function mgs:v5.0.0/zombies/barriers/on_remover_valid

execute if score #barrier_remover_valid mgs.data matches 1 run scoreboard players remove @s mgs.zb.barrier.r_timer 1
execute if score #barrier_remover_valid mgs.data matches 1 if score @s mgs.zb.barrier.r_timer matches 0 run function mgs:v5.0.0/zombies/barriers/destroy

# If not in range: check if remover still exists globally (alive but out of range = pause; gone = cancel)
execute if score #barrier_remover_valid mgs.data matches 0 as @e[tag=mgs.barrier_removing] if score @s mgs.zb.barrier.removing_id = #barrier_id mgs.data run scoreboard players set #barrier_remover_valid mgs.data 2
execute if score #barrier_remover_valid mgs.data matches 0 run function mgs:v5.0.0/zombies/barriers/cancel_remove

