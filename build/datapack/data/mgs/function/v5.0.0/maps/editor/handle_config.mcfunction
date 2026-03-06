
#> mgs:v5.0.0/maps/editor/handle_config
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/process_element
#

# Initialize enemy config with defaults if missing
execute unless data storage mgs:temp map_edit.map.enemy_config run data modify storage mgs:temp map_edit.map.enemy_config set value {level_1:{entity:"pillager",hp:20},level_2:{entity:"pillager",hp:40},level_3:{entity:"pillager",hp:60},level_4:{entity:"pillager",hp:80}}

tellraw @a[tag=mgs.map_editor] {"text":"============================================","color":"dark_gray"}
tellraw @a[tag=mgs.map_editor] [{"text":"","color":"white","bold":true},"  ⚙ ",{"translate": "mgs.enemy_configuration"}]
tellraw @a[tag=mgs.map_editor] {"text":"============================================","color":"dark_gray"}
tellraw @a[tag=mgs.map_editor] ["  ",{"translate": "mgs.level_1","color":"green","bold":true},{"text":": ","color":"gray"},{"storage":"mgs:temp","nbt":"map_edit.map.enemy_config.level_1.entity","color":"white"},{"text":" (HP: ","color":"gray"},{"storage":"mgs:temp","nbt":"map_edit.map.enemy_config.level_1.hp","color":"yellow"},{"text":")","color":"gray"}]
tellraw @a[tag=mgs.map_editor] ["    ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/data modify storage mgs:temp map_edit.map.enemy_config.level_1.entity set value \"pillager\""}, "hover_event": {"action": "show_text", "value": "Edit Level 1 entity type"}}, "Entity", "]"],{"text":" "},[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/data modify storage mgs:temp map_edit.map.enemy_config.level_1.hp set value 20"}, "hover_event": {"action": "show_text", "value": "Edit Level 1 HP"}}, "HP", "]"]]
tellraw @a[tag=mgs.map_editor] ["  ",{"translate": "mgs.level_2","color":"yellow","bold":true},{"text":": ","color":"gray"},{"storage":"mgs:temp","nbt":"map_edit.map.enemy_config.level_2.entity","color":"white"},{"text":" (HP: ","color":"gray"},{"storage":"mgs:temp","nbt":"map_edit.map.enemy_config.level_2.hp","color":"yellow"},{"text":")","color":"gray"}]
tellraw @a[tag=mgs.map_editor] ["    ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/data modify storage mgs:temp map_edit.map.enemy_config.level_2.entity set value \"pillager\""}, "hover_event": {"action": "show_text", "value": "Edit Level 2 entity type"}}, "Entity", "]"],{"text":" "},[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/data modify storage mgs:temp map_edit.map.enemy_config.level_2.hp set value 20"}, "hover_event": {"action": "show_text", "value": "Edit Level 2 HP"}}, "HP", "]"]]
tellraw @a[tag=mgs.map_editor] ["  ",{"translate": "mgs.level_3","color":"gold","bold":true},{"text":": ","color":"gray"},{"storage":"mgs:temp","nbt":"map_edit.map.enemy_config.level_3.entity","color":"white"},{"text":" (HP: ","color":"gray"},{"storage":"mgs:temp","nbt":"map_edit.map.enemy_config.level_3.hp","color":"yellow"},{"text":")","color":"gray"}]
tellraw @a[tag=mgs.map_editor] ["    ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/data modify storage mgs:temp map_edit.map.enemy_config.level_3.entity set value \"pillager\""}, "hover_event": {"action": "show_text", "value": "Edit Level 3 entity type"}}, "Entity", "]"],{"text":" "},[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/data modify storage mgs:temp map_edit.map.enemy_config.level_3.hp set value 20"}, "hover_event": {"action": "show_text", "value": "Edit Level 3 HP"}}, "HP", "]"]]
tellraw @a[tag=mgs.map_editor] ["  ",{"translate": "mgs.level_4","color":"red","bold":true},{"text":": ","color":"gray"},{"storage":"mgs:temp","nbt":"map_edit.map.enemy_config.level_4.entity","color":"white"},{"text":" (HP: ","color":"gray"},{"storage":"mgs:temp","nbt":"map_edit.map.enemy_config.level_4.hp","color":"yellow"},{"text":")","color":"gray"}]
tellraw @a[tag=mgs.map_editor] ["    ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/data modify storage mgs:temp map_edit.map.enemy_config.level_4.entity set value \"pillager\""}, "hover_event": {"action": "show_text", "value": "Edit Level 4 entity type"}}, "Entity", "]"],{"text":" "},[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/data modify storage mgs:temp map_edit.map.enemy_config.level_4.hp set value 20"}, "hover_event": {"action": "show_text", "value": "Edit Level 4 HP"}}, "HP", "]"]]
tellraw @a[tag=mgs.map_editor] {"text":"============================================","color":"dark_gray"}

