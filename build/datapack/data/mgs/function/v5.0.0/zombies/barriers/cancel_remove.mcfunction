
#> mgs:v5.0.0/zombies/barriers/cancel_remove
#
# @executed	positioned ^ ^ ^-1
#
# @within	mgs:v5.0.0/zombies/barriers/handle_removing
#

# @s = barrier display — remover left range or died
scoreboard players set @s mgs.zb.barrier.r_timer 0
execute as @e[tag=mgs.barrier_removing] if score @s mgs.zb.barrier.removing_id = #barrier_id mgs.data run tag @s remove mgs.barrier_removing

