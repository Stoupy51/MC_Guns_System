
#> mgs:v5.1.0/zombies/barricades/cancel_repair
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/handle_repair
#

# @s = barricade display — repairer stopped sneaking or left range
scoreboard players set @s mgs.zb.barricade.rp_timer 0
execute as @a[tag=mgs.barricade_repairing] if score @s mgs.zb.barricade.repairing_id = #barricade_id mgs.data run tag @s remove mgs.barricade_repairing

