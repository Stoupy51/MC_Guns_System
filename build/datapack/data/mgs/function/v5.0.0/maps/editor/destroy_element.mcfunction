
#> mgs:v5.0.0/maps/editor/destroy_element
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..3]
#
# @within	mgs:v5.0.0/maps/editor/handle_destroy [ at @s & as @n[tag=mgs.map_element,distance=..3] ]
#

# @s = the map_element marker to destroy
# Announce what was removed
execute if entity @s[tag=mgs.element.base_coordinates] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.base_coordinates_removed","color":"light_purple"}]
execute if entity @s[tag=mgs.element.red_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.red_spawn_removed","color":"red"}]
execute if entity @s[tag=mgs.element.blue_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.blue_spawn_removed","color":"blue"}]
execute if entity @s[tag=mgs.element.general_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.general_spawn_removed","color":"yellow"}]
execute if entity @s[tag=mgs.element.out_of_bounds] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.out_of_bounds_removed","color":"dark_red"}]
execute if entity @s[tag=mgs.element.boundary] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.boundary_corner_removed","color":"gray"}]
execute if entity @s[tag=mgs.element.search_and_destroy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.sd_objective_removed","color":"gold"}]
execute if entity @s[tag=mgs.element.domination] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.domination_point_removed","color":"green"}]
execute if entity @s[tag=mgs.element.hardpoint] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.hardpoint_zone_removed","color":"dark_purple"}]
execute if entity @s[tag=mgs.element.mission_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mission_spawn_removed","color":"aqua"}]
execute if entity @s[tag=mgs.element.enemy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.enemy_removed","color":"red"}]
execute if entity @s[tag=mgs.element.zombie_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.zombie_spawn_removed","color":"dark_green"}]
execute if entity @s[tag=mgs.element.player_spawn_zb] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.player_spawn_removed","color":"aqua"}]
execute if entity @s[tag=mgs.element.wallbuy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.wallbuy_removed","color":"yellow"}]
execute if entity @s[tag=mgs.element.door] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.door_removed","color":"gold"}]
execute if entity @s[tag=mgs.element.trap] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.trap_removed","color":"red"}]
execute if entity @s[tag=mgs.element.perk_machine] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.perk_machine_removed","color":"dark_purple"}]
execute if entity @s[tag=mgs.element.mystery_box_pos] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mystery_box_pos_removed","color":"light_purple"}]
execute if entity @s[tag=mgs.element.power_switch] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.power_switch_removed","color":"green"}]

# Show data dump if element has compound data (zb_object, enemy, spawn)
execute if data entity @s data run tellraw @a[tag=mgs.map_editor] ["  ",{"translate": "mgs.data","color":"gray"},{"entity":"@s","nbt":"data","color":"white"}]

# Kill the marker
kill @s

