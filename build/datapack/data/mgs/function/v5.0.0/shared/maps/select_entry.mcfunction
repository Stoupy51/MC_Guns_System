
#> mgs:v5.0.0/shared/maps/select_entry
#
# @within	mgs:v5.0.0/shared/maps/select_iter with storage mgs:temp _map_entry
#
# @args		name (unknown)
#			mode (unknown)
#			id (unknown)
#			description (unknown)
#

$tellraw @s ["","  ",{"text":""},{"text":"[$(name)]","color":"green","click_event":{"action":"suggest_command","command":"/data modify storage mgs:$(mode) game.map_id set value \"$(id)\""},"hover_event":{"action":"show_text","value":"Click to select '$(name)'"}},{"text":" - $(description)","color":"gray"}]

