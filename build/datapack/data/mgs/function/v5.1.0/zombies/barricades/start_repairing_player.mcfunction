
#> mgs:v5.1.0/zombies/barricades/start_repairing_player
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/find_repairer
#

# @s = player assigned as repairer
tag @s add mgs.barricade_repairing
scoreboard players operation @s mgs.zb.barricade.repairing_id = #barricade_id mgs.data
scoreboard players set #barricade_found_repairer mgs.data 1

