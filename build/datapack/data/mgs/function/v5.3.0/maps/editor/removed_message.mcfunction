
#> mgs:v5.3.0/maps/editor/removed_message
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..3]
#
# @within	mgs:v5.3.0/maps/editor/destroy_element with storage mgs:temp _ed_removed
#
# @args		id (unknown)
#

$tellraw @a[tag=mgs.map_editor] ["  ",[{"text": "[", "color": "green", "click_event": {"action": "run_command", "command": "/function mgs:v5.3.0/maps/editor/revert {id:$(id)}"}, "hover_event": {"action": "show_text", "value": "Put it back as it was"}}, "Revert", "]"],"  ",{"translate":"mgs.data_2","fallback":"Data: ","color":"gray"},{"storage":"mgs:temp","nbt":"_ed_removed.marker.data","color":"white"}]

