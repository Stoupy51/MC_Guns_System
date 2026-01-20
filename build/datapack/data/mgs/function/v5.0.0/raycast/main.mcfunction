
#> mgs:v5.0.0/raycast/main
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/player/shoot [ anchored eyes & positioned ^ ^ ^ ]
#

# Copy damage to temp storage to avoid modifying original for multiple pellets
data modify storage mgs:temp damage set from storage mgs:gun all.stats.damage

# Handle accuracy
tp @s ~ ~ ~ ~ ~
function mgs:v5.0.0/raycast/accuracy/apply_spread

# Scores to remember to only play a sound type once
scoreboard players set #played_water mgs.data 0
scoreboard players set #played_glass mgs.data 0
scoreboard players set #played_cloth mgs.data 0
scoreboard players set #played_dirt mgs.data 0
scoreboard players set #played_mud mgs.data 0
scoreboard players set #played_wood mgs.data 0
scoreboard players set #played_plant mgs.data 0
scoreboard players set #played_solid mgs.data 0
scoreboard players set #played_soft mgs.data 0
scoreboard players set #next_air_particle mgs.data 0

# Prepare arguments
data modify storage mgs:input with set value {}
data modify storage mgs:input with.blocks set value "function #bs.hitbox:callback/get_block_collision_with_fluid"
data modify storage mgs:input with.entities set value true
data modify storage mgs:input with.piercing set value 10
data modify storage mgs:input with.max_distance set value 128
data modify storage mgs:input with.ignored_blocks set value "#mgs:v5.0.0/empty"
data modify storage mgs:input with.on_hit_point set value "function mgs:v5.0.0/raycast/on_hit_point"
data modify storage mgs:input with.on_targeted_block set value "function mgs:v5.0.0/raycast/on_targeted_block"
data modify storage mgs:input with.on_targeted_entity set value "function mgs:v5.0.0/raycast/on_targeted_entity"

# Launch raycast with callbacks (https://docs.mcbookshelf.dev/en/latest/modules/raycast.html#run-the-raycast)
execute at @s run function #bs.raycast:run with storage mgs:input

# Kill marker
kill @s

