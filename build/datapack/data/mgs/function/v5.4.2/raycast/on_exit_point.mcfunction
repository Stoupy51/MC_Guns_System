
#> mgs:v5.4.2/raycast/on_exit_point
#
# @within	mgs:v5.4.2/dialog/close_then
#			string in mgs:v5.4.2/raycast/main
#

execute if score #is_entity_hit mgs.data matches 1 as @e[tag=mgs.raycast_target] run function mgs:v5.4.2/raycast/headshot_and_damage
scoreboard players set #is_entity_hit mgs.data 0

