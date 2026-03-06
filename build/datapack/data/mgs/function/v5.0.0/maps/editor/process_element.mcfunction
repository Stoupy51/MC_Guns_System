
#> mgs:v5.0.0/maps/editor/process_element
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/on_place [ as @n[tag=mgs.new_element] & at @s ]
#

# DESTROY handler
execute if entity @s[tag=mgs.element.destroy] run function mgs:v5.0.0/maps/editor/handle_destroy
execute if entity @s[tag=mgs.element.destroy] run return run kill @s

execute if entity @s[tag=mgs.element.base_coordinates] run function mgs:v5.0.0/maps/editor/handle_base
execute if entity @s[tag=mgs.element.base_coordinates] run return run kill @s

execute if entity @s[tag=mgs.element.red_spawn] run function mgs:v5.0.0/maps/editor/handle_spawn
execute if entity @s[tag=mgs.element.red_spawn] run return run kill @s

execute if entity @s[tag=mgs.element.blue_spawn] run function mgs:v5.0.0/maps/editor/handle_spawn
execute if entity @s[tag=mgs.element.blue_spawn] run return run kill @s

execute if entity @s[tag=mgs.element.general_spawn] run function mgs:v5.0.0/maps/editor/handle_spawn
execute if entity @s[tag=mgs.element.general_spawn] run return run kill @s

execute if entity @s[tag=mgs.element.out_of_bounds] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.out_of_bounds] run return run kill @s

execute if entity @s[tag=mgs.element.boundary] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.boundary] run return run kill @s

execute if entity @s[tag=mgs.element.search_and_destroy] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.search_and_destroy] run return run kill @s

execute if entity @s[tag=mgs.element.domination] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.domination] run return run kill @s

execute if entity @s[tag=mgs.element.hardpoint] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.hardpoint] run return run kill @s

execute if entity @s[tag=mgs.element.mission_spawn] run function mgs:v5.0.0/maps/editor/handle_spawn
execute if entity @s[tag=mgs.element.mission_spawn] run return run kill @s

execute if entity @s[tag=mgs.element.level_1_enemy] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.level_1_enemy] run return run kill @s

execute if entity @s[tag=mgs.element.level_2_enemy] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.level_2_enemy] run return run kill @s

execute if entity @s[tag=mgs.element.level_3_enemy] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.level_3_enemy] run return run kill @s

execute if entity @s[tag=mgs.element.level_4_enemy] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.level_4_enemy] run return run kill @s

execute if entity @s[tag=mgs.element.config] run function mgs:v5.0.0/maps/editor/handle_config
execute if entity @s[tag=mgs.element.config] run return run kill @s

# Fallback: unknown type
kill @s

