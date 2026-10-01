
#> mgs:v5.1.0/zombies/barricades/repair
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/handle_repair
#

# Run as the barricade display: destroyed to intact.
scoreboard players set @s mgs.zb.barricade.state 0
scoreboard players set @s mgs.zb.barricade.rp_timer 0

execute as @a[tag=mgs.barricade_repairing] if score @s mgs.zb.barricade.repairing_id = #barricade_id mgs.data run function mgs:v5.1.0/zombies/barricades/on_repair_complete_player

data modify entity @s block_state set from entity @s data.block_enabled

execute as @e[tag=mgs.barricade_removing] if score @s mgs.zb.barricade.removing_id = #barricade_id mgs.data run tag @s remove mgs.barricade_removing

particle minecraft:happy_villager ~ ~1 ~ 0.5 0.5 0.5 0 10
playsound mgs:zombies/barricade/slam block @a[distance=..32] ~ ~ ~ 1.0 1.0

