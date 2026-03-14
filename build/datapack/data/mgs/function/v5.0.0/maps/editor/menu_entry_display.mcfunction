
#> mgs:v5.0.0/maps/editor/menu_entry_display
#
# @within	mgs:v5.0.0/maps/editor/menu_entry with storage mgs:temp map_menu
#
# @args		name (unknown)
#			id (unknown)
#			idx (unknown)
#			mode (unknown)
#

$tellraw @s ["  ",{"text":"$(name)","color":"white"},{"text":" ($(id))","color":"gray"}," ",[{"text":"[","color":"yellow","click_event":{"action":"run_command","command":"/function mgs:v5.0.0/maps/editor/enter {idx:$(idx),mode:$(mode)}"},"hover_event":{"action":"show_text","value":"Edit this map"}},{"translate":"mgs.edit"},"]"]," ",[{"text":"[","color":"red","click_event":{"action":"run_command","command":"/function mgs:v5.0.0/maps/editor/delete {idx:$(idx),mode:$(mode)}"},"hover_event":{"action":"show_text","value":"Delete this map"}},{"translate":"mgs.delete"},"]"]]

