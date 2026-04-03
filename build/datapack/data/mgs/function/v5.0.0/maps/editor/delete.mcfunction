
#> mgs:v5.0.0/maps/editor/delete
#
# @within	mgs:v5.0.0/maps/editor/menu_entry_display {idx:$(idx),mode:$(mode)}"},"hover_event":{"action":"show_text","value":"Edit this map"}},{"translate":"mgs.edit"},"]"]," ",[{"text":"[","color":"red","click_event":{"action":"suggest_command","command":"/function mgs:v5.0.0/maps/editor/delete {idx:$(idx),mode:$(mode)}"},"hover_event":{"action":"show_text","value":"Delete this map"}},{"translate":"mgs.delete"},"]"]]
#
# @args		mode (unknown)
#			idx (unknown)
#

$data remove storage mgs:maps $(mode)[$(idx)]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_deleted","color":"red"}]

# Refresh menu for the same mode
$function mgs:v5.0.0/maps/editor/list/$(mode)

