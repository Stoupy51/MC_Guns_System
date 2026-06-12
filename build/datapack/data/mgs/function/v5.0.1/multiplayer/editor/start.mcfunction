
#> mgs:v5.0.1/multiplayer/editor/start
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#			mgs:v5.0.1/multiplayer/custom/edit
#

# Initialize Pick-10 budget
scoreboard players set @s mgs.mp.edit_points 10
# Mark editor as active (step 1 = picking primary)
scoreboard players set @s mgs.mp.edit_step 1
# Default to creating a new loadout (custom/edit overrides this after calling start)
scoreboard players set @s mgs.mp.edit_target 0

# Show primary weapon selection dialog
execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
function mgs:v5.0.1/multiplayer/editor/show_primary_dialog_macro with storage mgs:temp

