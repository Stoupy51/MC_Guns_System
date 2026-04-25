
#> mgs:v5.0.0/zombies/barriers/repair
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/handle_repair
#

# @s = destroyed barrier display → transitions back to intact
scoreboard players set @s mgs.zb.barrier.state 0
scoreboard players set @s mgs.zb.barrier.rp_timer 0

# Clean up repairing player tag and show success
execute as @a[tag=mgs.barrier_repairing] if score @s mgs.zb.barrier.repairing_id = #barrier_id mgs.data run function mgs:v5.0.0/zombies/barriers/on_repair_complete_player

# Switch back to enabled block state
data modify entity @s block_state set from entity @s data.block_enabled

# Clear any leftover barrier_removing tag from zombies associated with this barrier
execute as @e[tag=mgs.barrier_removing] if score @s mgs.zb.barrier.removing_id = #barrier_id mgs.data run tag @s remove mgs.barrier_removing

# Sound + particles
particle minecraft:happy_villager ~ ~1 ~ 0.5 0.5 0.5 0 10
playsound minecraft:block.anvil.use block @a ~ ~ ~ 1.0 1.5

