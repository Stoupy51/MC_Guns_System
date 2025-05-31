
#> mgs:v5.0.0/raycast/on_hit_point
#
# @within	mgs:v5.0.0/raycast/main
#

# If targeted entity, return to prevent showing particles
execute if data storage bs:lambda raycast.targeted_entity run return fail

# Get current block (https://docs.mcbookshelf.dev/en/latest/modules/block.html#get)
scoreboard players set #is_water mgs.data 0
scoreboard players set #is_pass_through mgs.data 0
data modify storage mgs:temp Pos set from entity @s Pos
data modify entity @s Pos set from storage bs:lambda raycast.targeted_block
execute at @s if block ~ ~ ~ #bs.hitbox:can_pass_through run scoreboard players set #is_pass_through mgs.data 1
execute at @s if block ~ ~ ~ #mgs:v5.0.0/sounds/water run scoreboard players set #is_water mgs.data 1
execute at @s run function #bs.block:get_block
data modify entity @s Pos set from storage mgs:temp Pos

# Make block particles (if not passing through)
data modify storage mgs:input with set value {x:0,y:0,z:0,block:"minecraft:air"}
data modify storage mgs:input with.block set from storage bs:out block.type
data modify storage mgs:input with.x set from storage bs:lambda raycast.hit_point[0]
data modify storage mgs:input with.y set from storage bs:lambda raycast.hit_point[1]
data modify storage mgs:input with.z set from storage bs:lambda raycast.hit_point[2]
execute if score #is_pass_through mgs.data matches 0 run return run function mgs:v5.0.0/raycast/block_particles with storage mgs:input with

# Change particles if passing through
execute if score #is_water mgs.data matches 1 run data modify storage mgs:input with.block set value "minecraft:bubble"
execute if score #is_water mgs.data matches 0 run data modify storage mgs:input with.block set value "minecraft:mycelium"

# Create particles every third iteration to maintain visual clarity while reducing particle density
scoreboard players add #next_air_particle mgs.data 1
execute if score #next_air_particle mgs.data matches 2 run function mgs:v5.0.0/raycast/air_particles with storage mgs:input with
execute if score #next_air_particle mgs.data matches 3.. run scoreboard players set #next_air_particle mgs.data 0

