
#> mgs:v5.0.0/maps/editor/handle_config_default_btn
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/handle_config with storage mgs:temp _cfg
#
# @args		default_fn (unknown)
#

$tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["    ",{"translate":"mgs.edit_function","color":"aqua","click_event":{"action":"suggest_command","command":"/data modify storage mgs:temp map_edit.map.default_enemy_function set value \"$(default_fn)\""},"hover_event":{"action":"show_text","value":"Click to edit the default spawn function for new enemies"}}]

