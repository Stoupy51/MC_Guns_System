
#> mgs:v5.0.0/maps/editor/exit
#
# @within	mgs:v5.0.0/maps/editor/enter "hover_event": {"action": "show_text", "value": "Save changes and exit editor"}}, "Save & Exit", "]"],{"text":" or "},[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/maps/editor/exit"}, "hover_event": {"action": "show_text", "value": "Discard changes and exit editor"}}, "Exit", "]"]]
#			mgs:v5.0.0/maps/editor/process_element [ as @p[tag=mgs.map_editor,distance=..6,sort=nearest] ]
#

execute unless score @s mgs.mp.map_edit matches 1 run return fail
function mgs:v5.0.0/maps/editor/cleanup
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.exited_map_editor_changes_discarded","color":"red"}]

