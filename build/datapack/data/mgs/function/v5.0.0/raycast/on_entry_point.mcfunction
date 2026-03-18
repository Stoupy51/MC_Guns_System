
#> mgs:v5.0.0/raycast/on_entry_point
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/raycast/main
#

# If targeted entity, return to prevent showing particles
execute if score #is_entity_hit mgs.data matches 1 run return 0
scoreboard players set #is_entity_hit mgs.data 0

# Make block particles (if not passing through) (on_targeted_block runs first to set passing through)
data modify storage mgs:input with set value {block:"minecraft:air"}
data modify storage mgs:input with.block set from storage mgs:temp block.type
execute if score #is_pass_through mgs.data matches 0 run return run function mgs:v5.0.0/raycast/block_particles with storage mgs:input with

# Change particles if passing through
execute if score #is_water mgs.data matches 1 run data modify storage mgs:input with.block set value "minecraft:bubble"
execute if score #is_water mgs.data matches 0 run data modify storage mgs:input with.block set value "minecraft:mycelium"

# Create particles every third iteration to maintain visual clarity while reducing particle density
scoreboard players add #next_air_particle mgs.data 1
execute if score #next_air_particle mgs.data matches 2 run function mgs:v5.0.0/raycast/air_particles with storage mgs:input with
execute if score #next_air_particle mgs.data matches 3.. run scoreboard players set #next_air_particle mgs.data 0

