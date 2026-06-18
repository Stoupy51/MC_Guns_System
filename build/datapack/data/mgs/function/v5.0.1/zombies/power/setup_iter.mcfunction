
#> mgs:v5.0.1/zombies/power/setup_iter
#
# @within	mgs:v5.0.1/zombies/power/setup
#			mgs:v5.0.1/zombies/power/setup_iter
#

# Read relative position and convert to absolute
execute store result score #pwx mgs.data run data get storage mgs:temp _pw_iter[0].pos[0]
execute store result score #pwy mgs.data run data get storage mgs:temp _pw_iter[0].pos[1]
execute store result score #pwz mgs.data run data get storage mgs:temp _pw_iter[0].pos[2]
scoreboard players operation #pwx mgs.data += #gm_base_x mgs.data
scoreboard players operation #pwy mgs.data += #gm_base_y mgs.data
scoreboard players operation #pwz mgs.data += #gm_base_z mgs.data

# Store absolute position for macro
execute store result storage mgs:temp _pw.x int 1 run scoreboard players get #pwx mgs.data
execute store result storage mgs:temp _pw.y int 1 run scoreboard players get #pwy mgs.data
execute store result storage mgs:temp _pw.z int 1 run scoreboard players get #pwz mgs.data

# Store yaw for the display (stored = player_yaw + 180; the model's fixed rotation -180 compensates,
# so the switch faces the placer just like the perk/PAP machine displays)
data modify storage mgs:temp _pw.yaw set value 0.0f
execute if data storage mgs:temp _pw_iter[0].rotation[0] run data modify storage mgs:temp _pw.yaw set from storage mgs:temp _pw_iter[0].rotation[0]

# Summon interaction entity + custom-model display
function mgs:v5.0.1/zombies/power/place_at with storage mgs:temp _pw

# Continue iteration
data remove storage mgs:temp _pw_iter[0]
execute if data storage mgs:temp _pw_iter[0] run function mgs:v5.0.1/zombies/power/setup_iter

