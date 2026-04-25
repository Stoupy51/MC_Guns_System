
#> mgs:v5.0.0/zombies/barriers/handle_removing
#
# @executed	positioned ^ ^ ^-1
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

# Not in range (dead or pushed out): always cancel so the zombie is freed
execute if score #barrier_remover_valid mgs.data matches 0 run function mgs:v5.0.0/zombies/barriers/cancel_remove

