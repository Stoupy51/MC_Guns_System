
#> mgs:v5.3.0/maps/editor/cleanup
#
# @executed	as @p[tag=mgs.map_editor,distance=..6,sort=nearest]
#
# @within	mgs:v5.3.0/maps/editor/save_exit
#			mgs:v5.3.0/maps/editor/exit
#

tag @s remove mgs.cs_abox

kill @e[tag=mgs.map_element]
kill @e[tag=mgs.editor_display]

scoreboard players set @s mgs.mp.map_edit 0
tag @s remove mgs.map_editor
function mgs:v5.3.0/maps/editor/next_session
execute unless entity @a[scores={mgs.mp.map_edit=1}] run data remove storage mgs:temp map_edit

clear @s

