
#> mgs:v5.0.0/raycast/headshot_and_damage
#
# @executed	as @e[tag=mgs.raycast_target]
#
# @within	mgs:v5.0.0/raycast/on_exit_point [ as @e[tag=mgs.raycast_target] ]
#

# Check if in head zone (Y above 1400 relative to entity), if not apply normal damage
scoreboard players set #is_headshot mgs.data 0
scoreboard players set #headshot_multiplier mgs.data 1000
execute unless score $raycast.entry_point.y bs.lambda matches 1400.. at @s run return run function mgs:v5.0.0/raycast/apply_damage

# Calculate center of trajectory through head: ((entry_x + exit_x) / 2, (entry_z + exit_z) / 2)
execute store result score #entry_x mgs.data run scoreboard players get $raycast.entry_point.x bs.lambda
execute store result score #entry_z mgs.data run scoreboard players get $raycast.entry_point.z bs.lambda
execute store result score #exit_x mgs.data run scoreboard players get $raycast.exit_point.x bs.lambda
execute store result score #exit_z mgs.data run scoreboard players get $raycast.exit_point.z bs.lambda

scoreboard players operation #exit_x mgs.data += #entry_x mgs.data
scoreboard players operation #exit_z mgs.data += #entry_z mgs.data
scoreboard players operation #exit_x mgs.data /= #2 mgs.data
scoreboard players operation #exit_z mgs.data /= #2 mgs.data

scoreboard players set #dist_sq mgs.data 0
scoreboard players operation #dist_sq mgs.data = #exit_x mgs.data
scoreboard players operation #dist_sq mgs.data *= #exit_x mgs.data
scoreboard players operation #exit_z mgs.data *= #exit_z mgs.data
scoreboard players operation #dist_sq mgs.data += #exit_z mgs.data

# Get sqrt: https://docs.mcbookshelf.dev/en/latest/modules/math/#square-root
data modify storage bs:in math.sqrt.x set value 0
execute store result storage bs:in math.sqrt.x float 0.000001 run scoreboard players get #dist_sq mgs.data
function #bs.math:sqrt
execute store result score #distance mgs.data run data get storage bs:out math.sqrt 1000

# Clamp distance to 500 (0.5 block)
execute if score #distance mgs.data matches 501.. run scoreboard players set #distance mgs.data 500

# Calculate multiplier: 2000 - (distance * 2)
scoreboard players set #headshot_multiplier mgs.data 2000
scoreboard players operation #distance mgs.data *= #2 mgs.data
scoreboard players operation #headshot_multiplier mgs.data -= #distance mgs.data

# Apply multiplier to damage
scoreboard players operation #damage mgs.data *= #headshot_multiplier mgs.data
scoreboard players operation #damage mgs.data /= #1000 mgs.data

# Apply damage
scoreboard players set #is_headshot mgs.data 1
execute at @s run function mgs:v5.0.0/raycast/apply_damage

