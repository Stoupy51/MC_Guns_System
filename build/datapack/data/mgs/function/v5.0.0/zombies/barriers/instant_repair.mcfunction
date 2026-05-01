
#> mgs:v5.0.0/zombies/barriers/instant_repair
#
# @executed	as @e[tag=mgs.barrier_display,scores={mgs.zb.barrier.state=1}] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/repair_all [ as @e[tag=mgs.barrier_display,scores={mgs.zb.barrier.state=1}] & at @s ]
#

# Set barrier to intact state
scoreboard players set @s mgs.zb.barrier.state 0

# Clear any in-progress remove / repair counters so no stale IDs linger
scoreboard players set @s mgs.zb.barrier.repairing_id 0
scoreboard players set @s mgs.zb.barrier.removing_id 0

# Release any zombie or player currently acting on this barrier
tag @e[tag=mgs.barrier_removing,scores={mgs.zb.barrier.removing_id=1..}] remove mgs.barrier_removing
tag @a[tag=mgs.barrier_repairing] remove mgs.barrier_repairing

# Re-enable the block (collision/visibility)
data modify entity @s block_state set from entity @s data.block_enabled

# Visual feedback
particle minecraft:happy_villager ~ ~ ~ 0.5 0.5 0.5 0.05 10 normal
playsound minecraft:block.wood.place block @a ~ ~ ~ 1.0 1.0

