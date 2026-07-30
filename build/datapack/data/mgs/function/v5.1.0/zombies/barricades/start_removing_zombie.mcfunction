
#> mgs:v5.1.0/zombies/barricades/start_removing_zombie
#
# @executed	positioned ^ ^ ^-1
#
# @within	mgs:v5.1.0/zombies/barricades/find_remover
#

# @s = zombie assigned as remover
tag @s add mgs.barricade_removing
scoreboard players operation @s mgs.zb.barricade.removing_id = #barricade_id mgs.data
scoreboard players set #barricade_found_remover mgs.data 1

