
#> mgs:v5.4.2/zombies/barricades/destroy
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/barricades/handle_removing
#

# Run as the barricade display: intact to destroyed.
function mgs:v5.4.2/zombies/barricades/break

execute as @e[tag=mgs.barricade_removing] if score @s mgs.zb.barricade.removing_id = #barricade_id mgs.data run tag @s remove mgs.barricade_removing

particle minecraft:large_smoke ~ ~0.5 ~ 0.4 0.4 0.4 0.02 6
particle minecraft:crit ~ ~0.5 ~ 0.4 0.4 0.4 0.05 8
playsound mgs:zombies/barricade/snap block @a[distance=..32] ~ ~ ~ 1.0 1.0

