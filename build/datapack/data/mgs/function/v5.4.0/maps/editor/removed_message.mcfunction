
#> mgs:v5.4.0/maps/editor/removed_message
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/destroy_element with storage mgs:temp _ed_removed
#
# @args		id (unknown)
#

$tellraw @a[tag=mgs.map_editor] ["  ",[{"text": "[", "color": "green", "click_event": {"action": "run_command", "command": "/function mgs:v5.4.0/maps/editor/revert {id:$(id)}"}, "hover_event": {"action": "show_text", "value": "Put it back as it was"}}, "Revert", "]"],"  ",{"translate":"mgs.data_2","fallback":"Data: ","color":"gray"},{"storage":"mgs:temp","nbt":"_ed_removed.marker.data","color":"white"}]

