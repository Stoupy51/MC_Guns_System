
#> mgs:v5.0.0/zombies/barriers/destroy
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/handle_removing
#

# @s = intact barrier display → transitions to destroyed
scoreboard players set @s mgs.zb.barrier.state 1
scoreboard players set @s mgs.zb.barrier.r_timer 0

# Clean up removing zombie
execute as @e[tag=mgs.barrier_removing] if score @s mgs.zb.barrier.removing_id = #barrier_id mgs.data run tag @s remove mgs.barrier_removing

# Switch to disabled block state
data modify entity @s block_state set from entity @s data.block_disabled

# Sound + particles
particle minecraft:large_smoke ~ ~0.5 ~ 0.4 0.4 0.4 0.02 6
particle minecraft:crit ~ ~0.5 ~ 0.4 0.4 0.4 0.05 8
playsound minecraft:entity.zombie.break_wooden_door block @a ~ ~ ~ 1.0 1.0

