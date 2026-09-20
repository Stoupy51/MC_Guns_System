
#> mgs:v5.1.0/zombies/barricades/find_remover
#
# @executed	positioned ^ ^ ^-1
#
# @within	mgs:v5.1.0/zombies/barricades/intact_tick with storage mgs:temp _btick
#
# @args		radius (unknown)
#

# MACRO: @s = intact barricade marker, $(radius) = sphere radius
# Picks nearest eligible zombie and assigns it as remover
scoreboard players set #barricade_found_remover mgs.data 0
$execute as @e[tag=mgs.zombie_round,tag=!mgs.barricade_removing,distance=..$(radius),limit=1,sort=nearest] run function mgs:v5.1.0/zombies/barricades/start_removing_zombie
execute if score #barricade_found_remover mgs.data matches 1 run scoreboard players set @s mgs.zb.barricade.r_timer 40

