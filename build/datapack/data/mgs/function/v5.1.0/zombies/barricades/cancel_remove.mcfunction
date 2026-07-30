
#> mgs:v5.1.0/zombies/barricades/cancel_remove
#
# @executed	positioned ^ ^ ^-1
#
# @within	mgs:v5.1.0/zombies/barricades/handle_removing
#

# @s = barricade display — remover left range or died
scoreboard players set @s mgs.zb.barricade.r_timer 0
execute as @e[tag=mgs.barricade_removing] if score @s mgs.zb.barricade.removing_id = #barricade_id mgs.data run tag @s remove mgs.barricade_removing

