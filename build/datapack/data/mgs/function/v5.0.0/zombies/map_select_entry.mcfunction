
#> mgs:v5.0.0/zombies/map_select_entry
#
# @within	mgs:v5.0.0/zombies/map_select with storage mgs:temp _map_iter[0]
#			mgs:v5.0.0/zombies/map_select_entry with storage mgs:temp _map_iter[0]
#
# @args		name (unknown)
#			id (unknown)
#			description (unknown)
#

$tellraw @s ["",{"text":"  "},{"text":"[$(name)]","color":"green","click_event":{"action":"run_command","command":"/data modify storage mgs:zombies game.map_id set value \"$(id)\""},"hover_event":{"action":"show_text","value":"Click to select '$(name)'"}},{"text":" - $(description)","color":"gray"}]

data remove storage mgs:temp _map_iter[0]
scoreboard players add #_map_idx mgs.data 1
execute if data storage mgs:temp _map_iter[0] run function mgs:v5.0.0/zombies/map_select_entry with storage mgs:temp _map_iter[0]

