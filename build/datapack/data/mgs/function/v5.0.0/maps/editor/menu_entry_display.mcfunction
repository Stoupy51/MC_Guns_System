
#> mgs:v5.0.0/maps/editor/menu_entry_display
#
# @within	mgs:v5.0.0/maps/editor/menu_entry with storage mgs:temp map_menu
#
# @args		name (unknown)
#			id (unknown)
#			idx (unknown)
#

$tellraw @s ["  ",{"text":"$(name)","color":"white"},{"text":" ($(id))","color":"gray"},{"text":" "},{"translate": "mgs.edit","color":"yellow","click_event":{"action":"run_command","command":"/function mgs:v5.0.0/maps/editor/enter {idx:$(idx)}"},"hover_event":{"action":"show_text","value":"Edit this map"}},{"text":" "},{"translate": "mgs.delete","color":"red","click_event":{"action":"run_command","command":"/function mgs:v5.0.0/maps/editor/delete {idx:$(idx)}"},"hover_event":{"action":"show_text","value":"Delete this map"}}]

