
#> mgs:v5.1.0/zombies/barricades/handle_removing
#
# @executed	positioned ^ ^ ^-1
#
# @within	mgs:v5.1.0/zombies/barricades/intact_tick with storage mgs:temp _btick
#
# @args		radius (unknown)
#

# Run as the barricade display; $(radius) is the sphere radius.
scoreboard players set #barricade_remover_valid mgs.data 0
$execute as @e[tag=mgs.barricade_removing,distance=..$(radius)] at @s if score @s mgs.zb.barricade.removing_id = #barricade_id mgs.data run function mgs:v5.1.0/zombies/barricades/on_remover_valid

execute if score #barricade_remover_valid mgs.data matches 1 run scoreboard players operation @s mgs.zb.barricade.r_timer -= #tick_delta mgs.data
execute if score #barricade_remover_valid mgs.data matches 1 unless score @s mgs.zb.barricade.r_timer matches 0.. run scoreboard players set @s mgs.zb.barricade.r_timer 0
execute if score #barricade_remover_valid mgs.data matches 1 if score @s mgs.zb.barricade.r_timer matches 0 run function mgs:v5.1.0/zombies/barricades/destroy

# Out of range (dead or pushed away): cancel so the zombie is freed.
execute if score #barricade_remover_valid mgs.data matches 0 run function mgs:v5.1.0/zombies/barricades/cancel_remove

