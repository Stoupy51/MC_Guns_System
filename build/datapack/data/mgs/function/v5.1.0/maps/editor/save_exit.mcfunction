
#> mgs:v5.1.0/maps/editor/save_exit
#
# @executed	as @p[tag=mgs.map_editor,distance=..6,sort=nearest]
#
# @within	string in mgs:v5.1.0/maps/editor/enter
#			mgs:v5.1.0/maps/editor/process_element [ as @p[tag=mgs.map_editor,distance=..6,sort=nearest] ]
#

execute unless score @s mgs.mp.map_edit matches 1 run return fail

function mgs:v5.1.0/maps/editor/do_save

function mgs:v5.1.0/maps/editor/cleanup
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_saved_and_editor_closed","color":"green"}]

