
#> mgs:v5.1.0/zombies/barricades/instant_repair
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/repair_all [ at @s ]
#

# Set barricade to intact state
scoreboard players set @s mgs.zb.barricade.state 0

# Clear any in-progress remove / repair counters so no stale IDs linger
scoreboard players set @s mgs.zb.barricade.repairing_id 0
scoreboard players set @s mgs.zb.barricade.removing_id 0

# Release any zombie or player currently acting on this barricade
tag @e[tag=mgs.barricade_removing,scores={mgs.zb.barricade.removing_id=1..}] remove mgs.barricade_removing
tag @a[tag=mgs.barricade_repairing] remove mgs.barricade_repairing

# Re-enable the block (collision/visibility)
data modify entity @s block_state set from entity @s data.block_enabled

# Visual feedback
particle minecraft:happy_villager ~ ~ ~ 0.5 0.5 0.5 0.05 10 normal
playsound minecraft:block.wood.place block @a[distance=..32] ~ ~ ~ 1.0 1.0

