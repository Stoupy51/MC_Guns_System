
#> mgs:v5.0.0/raycast/on_hit_point
#
# @within	mgs:v5.0.0/raycast/main
#

# If targeted entity, return to prevent showing particles
execute if data storage bs:lambda raycast.targeted_entity run return fail

# Get current block (https://docs.mcbookshelf.dev/en/latest/modules/block.html#get)
data modify storage mgs:temp Pos set from entity @s Pos
data modify entity @s Pos set from storage bs:lambda raycast.targeted_block
execute at @s run function #bs.block:get_block
data modify entity @s Pos set from storage mgs:temp Pos

# Make block particles
data modify storage mgs:input with set value {x:0,y:0,z:0,block:"minecraft:air"}
data modify storage mgs:input with.block set from storage bs:out block.type
data modify storage mgs:input with.x set from storage bs:lambda raycast.hit_point[0]
data modify storage mgs:input with.y set from storage bs:lambda raycast.hit_point[1]
data modify storage mgs:input with.z set from storage bs:lambda raycast.hit_point[2]
execute unless data storage mgs:input with{block:"minecraft:air"} run return run function mgs:v5.0.0/raycast/block_particles with storage mgs:input with

