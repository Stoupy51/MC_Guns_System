
#> mgs:v5.0.0/maps/editor/handle_config_nearest_respawn_command_btn
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/handle_config with storage mgs:temp _cfg
#
# @args		nearest_cmd (unknown)
#

tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] {"text":"============================================","color":"dark_gray"}
tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["  ",{"translate":"mgs.nearest_respawn_command","color":"yellow","bold":true},{"entity":"@n[tag=mgs.element.respawn_command,distance=..10]","nbt":"data.command","color":"white"}]
$tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["    ",{"translate":"mgs.edit_nearest_respawn_command","color":"yellow","click_event":{"action":"suggest_command","command":"/data modify entity @n[tag=mgs.element.respawn_command,distance=..10] data.command set value \"$(nearest_cmd)\""},"hover_event":{"action":"show_text","value":"Edit nearest respawn command command using its current value"}}]

