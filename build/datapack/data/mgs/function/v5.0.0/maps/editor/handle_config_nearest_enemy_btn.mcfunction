
#> mgs:v5.0.0/maps/editor/handle_config_nearest_enemy_btn
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/handle_config with storage mgs:temp _cfg
#
# @args		nearest_fn (unknown)
#

tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] {"text":"============================================","color":"dark_gray"}
tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["  ",{"translate":"mgs.nearest_enemy","color":"yellow","bold":true},{"entity":"@n[tag=mgs.element.enemy,distance=..10]","nbt":"data.function","color":"white"}]
$tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["    ",{"translate":"mgs.edit_nearest_enemy","color":"yellow","click_event":{"action":"suggest_command","command":"/data modify entity @n[tag=mgs.element.enemy,distance=..10] data.function set value \"$(nearest_fn)\""},"hover_event":{"action":"show_text","value":"Edit nearest enemy using its current function"}}]

