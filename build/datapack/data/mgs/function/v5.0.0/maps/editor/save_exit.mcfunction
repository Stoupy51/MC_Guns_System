
#> mgs:v5.0.0/maps/editor/save_exit
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/process_element
#

# Only process if in editor mode
execute unless score @s mgs.mp.map_edit matches 1 run return fail

# Do the actual save
function mgs:v5.0.0/maps/editor/do_save

# Cleanup and exit
function mgs:v5.0.0/maps/editor/cleanup
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.map_saved_and_editor_closed","color":"green"}]

