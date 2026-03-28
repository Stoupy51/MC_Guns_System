
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
data modify storage mgs:temp _cfg.default_fn set from storage mgs:temp map_edit.map.default_enemy_function
function mgs:v5.0.0/maps/editor/handle_config_default_btn with storage mgs:temp _cfg
tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] ["  ",{"translate":"mgs.edit_the_function_path_above_then_run_the_command","color":"dark_gray","italic":true}]

execute if entity @e[tag=mgs.element.enemy,distance=..10] run data modify storage mgs:temp _cfg.default_fn set from storage mgs:temp map_edit.map.default_enemy_function
execute if entity @e[tag=mgs.element.enemy,distance=..10] run data modify storage mgs:temp _cfg.nearest_fn set from entity @n[tag=mgs.element.enemy,distance=..10] data.function
execute if entity @e[tag=mgs.element.enemy,distance=..10] run function mgs:v5.0.0/maps/editor/handle_config_nearest_enemy_btn with storage mgs:temp _cfg
execute if entity @e[tag=mgs.element.start_command,distance=..10] run data modify storage mgs:temp _cfg.nearest_cmd set from entity @n[tag=mgs.element.start_command,distance=..10] data.command
execute if entity @e[tag=mgs.element.start_command,distance=..10] run function mgs:v5.0.0/maps/editor/handle_config_nearest_start_command_btn with storage mgs:temp _cfg
execute if entity @e[tag=mgs.element.respawn_command,distance=..10] run data modify storage mgs:temp _cfg.nearest_cmd set from entity @n[tag=mgs.element.respawn_command,distance=..10] data.command
execute if entity @e[tag=mgs.element.respawn_command,distance=..10] run function mgs:v5.0.0/maps/editor/handle_config_nearest_respawn_command_btn with storage mgs:temp _cfg
tellraw @p[tag=mgs.map_editor,distance=..6,sort=nearest] {"text":"============================================","color":"dark_gray"}

