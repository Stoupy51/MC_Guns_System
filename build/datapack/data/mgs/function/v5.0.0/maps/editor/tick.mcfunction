
#> mgs:v5.0.0/maps/editor/tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Only run for players in editor mode
execute unless score @s mgs.mp.map_edit matches 1 run return fail

# Show particles at each element type & their yaw
execute as @e[tag=mgs.map_element] run data modify entity @s Rotation[0] set from entity @s data.yaw
execute as @e[tag=mgs.map_element] at @s positioned ^ ^ ^0.5 run particle dust{color:[1.0,1.0,1.0],scale:0.5} ~ ~1.69 ~ 0.1 0.1 0.1 0 5
execute at @e[tag=mgs.map_element,tag=mgs.element.base_coordinates] run particle dust{color:[1.0,0.0,1.0],scale:1.5} ~ ~1 ~ 0.3 0.5 0.3 0 5
execute at @e[tag=mgs.map_element,tag=mgs.element.red_spawn] run particle dust{color:[1.0,0.2,0.2],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.blue_spawn] run particle dust{color:[0.2,0.2,1.0],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.general_spawn] run particle dust{color:[1.0,1.0,0.2],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.boundary] run particle dust{color:[0.8,0.8,0.8],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.out_of_bounds] run particle dust{color:[0.6,0.0,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.search_and_destroy] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.domination] run particle dust{color:[0.0,1.0,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.hardpoint] run particle dust{color:[0.5,0.0,0.5],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3

# Actionbar: show info when near an element (within 5 blocks)
execute if entity @e[tag=mgs.map_element,tag=mgs.element.base_coordinates,distance=..5] run return run title @s actionbar [{"translate": "mgs.base_coordinates","color":"light_purple"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.boundary,distance=..5] run return run title @s actionbar [{"translate": "mgs.boundary_corner","color":"gray"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.out_of_bounds,distance=..5] run return run title @s actionbar [{"translate": "mgs.out_of_bounds","color":"dark_red"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.search_and_destroy,distance=..5] run return run title @s actionbar [{"translate": "mgs.sd_objective","color":"gold"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.domination,distance=..5] run return run title @s actionbar [{"translate": "mgs.domination_point","color":"green"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.hardpoint,distance=..5] run return run title @s actionbar [{"translate": "mgs.hardpoint_zone","color":"dark_purple"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.red_spawn,distance=..5] run return run title @s actionbar [{"translate": "mgs.red_spawn","color":"red"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.blue_spawn,distance=..5] run return run title @s actionbar [{"translate": "mgs.blue_spawn","color":"blue"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.general_spawn,distance=..5] run return run title @s actionbar [{"translate": "mgs.general_spawn","color":"yellow"}]

