
#> mgs:v5.4.2/maps/editor/cleanup
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/save_exit
#			mgs:v5.4.2/maps/editor/exit
#

tag @s remove mgs.cs_abox

scoreboard players set @s mgs.mp.map_edit 0
tag @s remove mgs.map_editor

# The other editors keep the session, its markers and its loaded chunks.
execute unless entity @a[tag=mgs.map_editor] run kill @e[tag=mgs.map_element]
execute unless entity @a[tag=mgs.map_editor] run kill @e[tag=mgs.editor_display]
execute unless entity @a[tag=mgs.map_editor] run function mgs:v5.4.2/maps/editor/release_kept
execute unless entity @a[tag=mgs.map_editor] run function mgs:v5.4.2/maps/editor/force_unload with storage mgs:temp map_edit.force
function mgs:v5.4.2/maps/editor/next_session
execute unless entity @a[scores={mgs.mp.map_edit=1}] run data remove storage mgs:temp map_edit

clear @s

