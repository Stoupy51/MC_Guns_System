
#> mgs:v5.2.0/maps/editor/exit
#
# @executed	as @p[tag=mgs.map_editor,distance=..6,sort=nearest]
#
# @within	string in mgs:v5.2.0/maps/editor/enter
#			mgs:v5.2.0/maps/editor/process_element [ as @p[tag=mgs.map_editor,distance=..6,sort=nearest] ]
#

execute unless score @s mgs.mp.map_edit matches 1 run return fail
function mgs:v5.2.0/maps/editor/cleanup
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.exited_map_editor_changes_discarded","fallback":"Exited map editor (changes discarded).","color":"red"}]

