
#> mgs:v5.0.0/zombies/power/setup_iter
#
# @within	mgs:v5.0.0/zombies/power/setup
#			mgs:v5.0.0/zombies/power/setup_iter
#

# Read relative position and convert to absolute
execute store result score #_pwx mgs.data run data get storage mgs:temp _pw_iter[0].pos[0]
execute store result score #_pwy mgs.data run data get storage mgs:temp _pw_iter[0].pos[1]
execute store result score #_pwz mgs.data run data get storage mgs:temp _pw_iter[0].pos[2]
scoreboard players operation #_pwx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_pwy mgs.data += #gm_base_y mgs.data
scoreboard players operation #_pwz mgs.data += #gm_base_z mgs.data

# Store absolute position for macro
execute store result storage mgs:temp _pw.x int 1 run scoreboard players get #_pwx mgs.data
execute store result storage mgs:temp _pw.y int 1 run scoreboard players get #_pwy mgs.data
execute store result storage mgs:temp _pw.z int 1 run scoreboard players get #_pwz mgs.data

# Determine lever facing from stored yaw (stored = player_yaw + 180)
execute store result score #_pw_yaw mgs.data run data get storage mgs:temp _pw_iter[0].rotation[0]
data modify storage mgs:temp _pw.facing set value "north"
execute if score #_pw_yaw mgs.data matches 0..44 run data modify storage mgs:temp _pw.facing set value "south"
execute if score #_pw_yaw mgs.data matches 315..360 run data modify storage mgs:temp _pw.facing set value "south"
execute if score #_pw_yaw mgs.data matches 45..134 run data modify storage mgs:temp _pw.facing set value "west"
execute if score #_pw_yaw mgs.data matches 225..314 run data modify storage mgs:temp _pw.facing set value "east"

# Place lever and summon interaction entity
function mgs:v5.0.0/zombies/power/place_at with storage mgs:temp _pw

# Continue iteration
data remove storage mgs:temp _pw_iter[0]
execute if data storage mgs:temp _pw_iter[0] run function mgs:v5.0.0/zombies/power/setup_iter

