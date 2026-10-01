
#> mgs:v5.1.0/zombies/barricades/instant_repair
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/repair_all [ at @s ]
#

scoreboard players set @s mgs.zb.barricade.state 0

scoreboard players set @s mgs.zb.barricade.repairing_id 0
scoreboard players set @s mgs.zb.barricade.removing_id 0

# Release any zombie or player acting on it.
tag @e[tag=mgs.barricade_removing,scores={mgs.zb.barricade.removing_id=1..}] remove mgs.barricade_removing
tag @a[tag=mgs.barricade_repairing] remove mgs.barricade_repairing

# Collision and visibility back.
data modify entity @s block_state set from entity @s data.block_enabled

# One slam per barricade: Carpenter reads as the whole map boarded up at once. No budget, it is rare and lasts one tick.
particle minecraft:happy_villager ~ ~ ~ 0.5 0.5 0.5 0.05 10 normal
playsound mgs:zombies/barricade/slam block @a[distance=..32] ~ ~ ~ 1.0 1.0

