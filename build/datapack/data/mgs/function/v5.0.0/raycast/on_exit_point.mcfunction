
#> mgs:v5.0.0/raycast/on_exit_point
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/raycast/main
#

# If entity, calculate headshot and apply damage to entity
execute if score #is_entity_hit mgs.data matches 1 as @e[tag=mgs.raycast_target] run function mgs:v5.0.0/raycast/headshot_and_damage
scoreboard players set #is_entity_hit mgs.data 0

