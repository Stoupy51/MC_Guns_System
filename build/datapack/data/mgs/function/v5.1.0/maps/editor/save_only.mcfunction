
#> mgs:v5.1.0/maps/editor/save_only
#
# @executed	as @p[tag=mgs.map_editor,distance=..6,sort=nearest]
#
# @within	mgs:v5.1.0/maps/editor/process_element [ as @p[tag=mgs.map_editor,distance=..6,sort=nearest] ]
#

execute unless score @s mgs.mp.map_edit matches 1 run return fail

function mgs:v5.1.0/maps/editor/do_save

# The save clears the tools.
function mgs:v5.1.0/maps/editor/give_tools

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_saved","color":"green"}]

