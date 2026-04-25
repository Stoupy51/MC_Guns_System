
#> mgs:v5.0.0/zombies/barriers/handle_repair
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/destroyed_tick with storage mgs:temp _brptick
#
# @args		radius (unknown)
#

# MACRO: @s = destroyed barrier marker, $(radius) = sphere radius
# Verify assigned repairer is still valid (sneaking, in range, correct id)
execute store result score #barrier_rp_cur mgs.data run scoreboard players get @s mgs.zb.barrier.rp_timer
scoreboard players set #barrier_repair_valid mgs.data 0
$execute as @a[tag=mgs.barrier_repairing,distance=..$(radius)] if score @s mgs.zb.barrier.repairing_id = #barrier_id mgs.data if predicate mgs:v5.0.0/is_sneaking run function mgs:v5.0.0/zombies/barriers/on_repairer_valid

execute if score #barrier_repair_valid mgs.data matches 0 run function mgs:v5.0.0/zombies/barriers/cancel_repair
execute if score #barrier_repair_valid mgs.data matches 1 run scoreboard players remove @s mgs.zb.barrier.rp_timer 1
execute if score #barrier_repair_valid mgs.data matches 1 if score @s mgs.zb.barrier.rp_timer matches 0 run function mgs:v5.0.0/zombies/barriers/repair

