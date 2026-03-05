
#> mgs:v5.0.0/maps/editor/process_element
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/on_place [ as @n[tag=mgs.new_element] & at @s ]
#

# Determine element type from tags and dispatch

# DESTROY handler
execute if entity @s[tag=mgs.element.destroy] run function mgs:v5.0.0/maps/editor/handle_destroy
execute if entity @s[tag=mgs.element.destroy] run return run kill @s

# Base coordinates handler
execute if entity @s[tag=mgs.element.base_coordinates] run function mgs:v5.0.0/maps/editor/handle_base
execute if entity @s[tag=mgs.element.base_coordinates] run return run kill @s

# Spawn handlers (need rotation from nearest player)
execute if entity @s[tag=mgs.element.red_spawn] run function mgs:v5.0.0/maps/editor/handle_spawn
execute if entity @s[tag=mgs.element.red_spawn] run return run kill @s

execute if entity @s[tag=mgs.element.blue_spawn] run function mgs:v5.0.0/maps/editor/handle_spawn
execute if entity @s[tag=mgs.element.blue_spawn] run return run kill @s

execute if entity @s[tag=mgs.element.general_spawn] run function mgs:v5.0.0/maps/editor/handle_spawn
execute if entity @s[tag=mgs.element.general_spawn] run return run kill @s

# Point-based handlers (no rotation)
execute if entity @s[tag=mgs.element.boundary] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.boundary] run return run kill @s

execute if entity @s[tag=mgs.element.out_of_bounds] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.out_of_bounds] run return run kill @s

execute if entity @s[tag=mgs.element.search_and_destroy] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.search_and_destroy] run return run kill @s

execute if entity @s[tag=mgs.element.domination] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.domination] run return run kill @s

execute if entity @s[tag=mgs.element.hardpoint] run function mgs:v5.0.0/maps/editor/handle_point
execute if entity @s[tag=mgs.element.hardpoint] run return run kill @s

# Fallback: unknown type, just kill
kill @s

