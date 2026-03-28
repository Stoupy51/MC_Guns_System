
#> mgs:v5.0.0/maps/editor/handle_config
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/process_element
#

# Initialize default enemy function if missing
execute unless data storage mgs:temp map_edit.map.default_enemy_function run data modify storage mgs:temp map_edit.map.default_enemy_function set value "mgs:v5.0.0/mob/default/level_1 {\"entity\":\"pillager\"}"

tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] {"text":"============================================","color":"dark_gray"}
tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] [{"text":"","color":"white","bold":true},"  ⚙ ",{"translate":"mgs.enemy_configuration"}]
tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] {"text":"============================================","color":"dark_gray"}
tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["  ",{"translate":"mgs.default_function","color":"gray"},{"storage":"mgs:temp","nbt":"map_edit.map.default_enemy_function","color":"white"}]
tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["    ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/data modify storage mgs:temp map_edit.map.default_enemy_function set value \"mgs:v5.0.0/mob/default/level_1 {'entity':'pillager'}\""}, "hover_event": {"action": "show_text", "value": "Click to edit the default spawn function for new enemies"}}, "Edit Function", "]"]]
tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["  ",{"translate":"mgs.edit_the_function_path_above_then_run_the_command","color":"dark_gray","italic":true}]

execute if entity @e[tag=mgs.element.enemy,distance=..10] run tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] {"text":"============================================","color":"dark_gray"}
execute if entity @e[tag=mgs.element.enemy,distance=..10] run tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["  ",{"translate":"mgs.nearest_enemy","color":"yellow","bold":true},{"entity":"@n[tag=mgs.element.enemy,distance=..10]","nbt":"data.function","color":"white"}]
execute if entity @e[tag=mgs.element.enemy,distance=..10] run tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["    ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/data modify entity @n[tag=mgs.element.enemy,distance=..10] data.function set from storage mgs:temp map_edit.map.default_enemy_function"}, "hover_event": {"action": "show_text", "value": "Apply current default function to nearest enemy"}}, "Edit Nearest Enemy", "]"]]
tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] {"text":"============================================","color":"dark_gray"}

