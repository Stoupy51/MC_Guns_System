
#> mgs:v5.1.0/zombies/barricades/handle_repair
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/destroyed_tick with storage mgs:temp _brptick
#
# @args		radius (unknown)
#

# MACRO: @s = destroyed barricade marker, $(radius) = sphere radius
# Verify assigned repairer is still valid (sneaking, in range, correct id)
execute store result score #barricade_rp_cur mgs.data run scoreboard players get @s mgs.zb.barricade.rp_timer
scoreboard players set #barricade_repair_valid mgs.data 0
$execute as @a[tag=mgs.barricade_repairing,distance=..$(radius)] if score @s mgs.zb.barricade.repairing_id = #barricade_id mgs.data if predicate mgs:v5.1.0/is_sneaking run function mgs:v5.1.0/zombies/barricades/on_repairer_valid

execute if score #barricade_repair_valid mgs.data matches 0 run function mgs:v5.1.0/zombies/barricades/cancel_repair
execute if score #barricade_repair_valid mgs.data matches 1 run scoreboard players operation @s mgs.zb.barricade.rp_timer -= #tick_delta mgs.data
execute if score #barricade_repair_valid mgs.data matches 1 unless score @s mgs.zb.barricade.rp_timer matches 0.. run scoreboard players set @s mgs.zb.barricade.rp_timer 0
execute if score #barricade_repair_valid mgs.data matches 1 if score @s mgs.zb.barricade.rp_timer matches 0 run function mgs:v5.1.0/zombies/barricades/repair

