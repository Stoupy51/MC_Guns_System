
#> mgs:v5.3.0/maps/editor/menu_entry_display
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/maps/editor/menu_entry with storage mgs:temp map_menu
#
# @args		name (unknown)
#			id (unknown)
#			idx (unknown)
#			mode (unknown)
#

$tellraw @s ["  ",{"text":"$(name)","color":"white"},{"text":" ($(id))","color":"gray"}," ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.3.0/maps/editor/enter {idx:$(idx),mode:$(mode)}"}, "hover_event": {"action": "show_text", "value": "Edit this map"}}, "Edit", "]"]," ",[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/function mgs:v5.3.0/maps/editor/settings {idx:$(idx),mode:$(mode)}"}, "hover_event": {"action": "show_text", "value": "Name, description and dimension"}}, "Settings", "]"]," ",[{"text": "[", "color": "green", "click_event": {"action": "run_command", "command": "/function mgs:v5.3.0/maps/editor/duplicate {idx:$(idx),mode:$(mode)}"}, "hover_event": {"action": "show_text", "value": "Copy this map under a new id"}}, "Duplicate", "]"]," ",[{"text": "[", "color": "light_purple", "click_event": {"action": "run_command", "command": "/function mgs:v5.3.0/maps/editor/export {idx:$(idx),mode:$(mode)}"}, "hover_event": {"action": "show_text", "value": "Show this map's data, ready to copy"}}, "Export", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "run_command", "command": "/function mgs:v5.3.0/maps/editor/delete_confirm {idx:$(idx),mode:$(mode)}"}, "hover_event": {"action": "show_text", "value": "Delete this map"}}, "Delete", "]"]]

