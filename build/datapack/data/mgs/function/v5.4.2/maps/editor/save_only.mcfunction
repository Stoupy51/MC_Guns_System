
#> mgs:v5.4.2/maps/editor/save_only
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/process_element [ as @p[tag=mgs.map_editor,distance=..6,sort=nearest] ]
#

execute unless score @s mgs.mp.map_edit matches 1 run return fail

execute unless function mgs:v5.4.2/maps/editor/do_save run return fail

# The save clears the tools.
function mgs:v5.4.2/maps/editor/give_tools

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.map_saved","fallback":"Map saved!","color":"green"}]

