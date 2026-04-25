
#> mgs:v5.0.0/zombies/barriers/cancel_repair
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/handle_repair
#

# @s = barrier display — repairer stopped sneaking or left range
scoreboard players set @s mgs.zb.barrier.rp_timer 0
execute as @a[tag=mgs.barrier_repairing] if score @s mgs.zb.barrier.repairing_id = #barrier_id mgs.data run tag @s remove mgs.barrier_repairing

