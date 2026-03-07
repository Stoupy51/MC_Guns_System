
#> mgs:v5.0.0/maps/editor/tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Only run for players in editor mode
execute unless score @s mgs.mp.map_edit matches 1 run return fail

# Mode switcher: detect right-click on warped fungus on a stick
execute if score @s mgs.class_menu matches 1.. if items entity @s weapon.mainhand *[custom_data~{mgs:{mode_switcher:true}}] run function mgs:v5.0.0/maps/editor/cycle_mode

# Show rotation indicator for all markers
execute as @e[tag=mgs.map_element] run data modify entity @s Rotation[0] set from entity @s data.yaw
execute as @e[tag=mgs.map_element] at @s positioned ^ ^ ^0.5 run particle dust{color:[1.0,1.0,1.0],scale:0.5} ~ ~1.69 ~ 0.1 0.1 0.1 0 5

# Per-element particles
execute at @e[tag=mgs.map_element,tag=mgs.element.base_coordinates] run particle dust{color:[1.0,0.0,1.0],scale:1.5} ~ ~1 ~ 0.3 0.5 0.3 0 5
execute at @e[tag=mgs.map_element,tag=mgs.element.red_spawn] run particle dust{color:[1.0,0.2,0.2],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.blue_spawn] run particle dust{color:[0.2,0.2,1.0],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.general_spawn] run particle dust{color:[1.0,1.0,0.2],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.out_of_bounds] run particle dust{color:[0.6,0.0,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.boundary] run particle dust{color:[0.8,0.8,0.8],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.search_and_destroy] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.domination] run particle dust{color:[0.0,1.0,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.hardpoint] run particle dust{color:[0.5,0.0,0.5],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.mission_spawn] run particle dust{color:[0.0,1.0,1.0],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 3
execute at @e[tag=mgs.map_element,tag=mgs.element.enemy] run particle dust{color:[1.0,0.2,0.2],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 3

# Actionbar: show info when near an element (within 5 blocks)
execute if entity @e[tag=mgs.map_element,tag=mgs.element.base_coordinates,distance=..5] run return run title @s actionbar [{"text":"⬟ ","color":"light_purple"},{"translate": "mgs.base_coordinates"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.red_spawn,distance=..5] run return run title @s actionbar [{"text":"● ","color":"red"},{"translate": "mgs.red_spawn"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.blue_spawn,distance=..5] run return run title @s actionbar [{"text":"● ","color":"blue"},{"translate": "mgs.blue_spawn"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.general_spawn,distance=..5] run return run title @s actionbar [{"text":"● ","color":"yellow"},{"translate": "mgs.general_spawn"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.out_of_bounds,distance=..5] run return run title @s actionbar [{"text":"☠ ","color":"dark_red"},{"translate": "mgs.out_of_bounds"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.boundary,distance=..5] run return run title @s actionbar [{"text":"◻ ","color":"gray"},{"translate": "mgs.boundary_corner"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.search_and_destroy,distance=..5] run return run title @s actionbar [{"text":"💣 ","color":"gold"},{"translate": "mgs.sd_objective"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.domination,distance=..5] run return run title @s actionbar [{"text":"🏴 ","color":"green"},{"translate": "mgs.domination_point"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.hardpoint,distance=..5] run return run title @s actionbar [{"text":"⚡ ","color":"dark_purple"},{"translate": "mgs.hardpoint_zone"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.mission_spawn,distance=..5] run return run title @s actionbar [{"text":"● ","color":"aqua"},{"translate": "mgs.mission_spawn"}]
execute if entity @e[tag=mgs.map_element,tag=mgs.element.enemy,distance=..5] run return run title @s actionbar [{"text":"👤 ","color":"red"},{"translate": "mgs.enemy"}]

