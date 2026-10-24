
#> mgs:v5.2.0/maps/editor/destroy_element
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..3]
#
# @within	mgs:v5.2.0/maps/editor/handle_destroy [ at @s & as @n[tag=mgs.map_element,distance=..3] ]
#

# Run as the marker to destroy.
execute if entity @s[tag=mgs.element.base_coordinates] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.base_coordinates_removed","fallback":"Base Coordinates removed!","color":"light_purple"}]
execute if entity @s[tag=mgs.element.red_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red_spawn_removed","fallback":"Red Spawn removed!","color":"red"}]
execute if entity @s[tag=mgs.element.blue_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.blue_spawn_removed","fallback":"Blue Spawn removed!","color":"blue"}]
execute if entity @s[tag=mgs.element.general_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.general_spawn_removed","fallback":"General Spawn removed!","color":"yellow"}]
execute if entity @s[tag=mgs.element.out_of_bounds] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.out_of_bounds_removed","fallback":"Out of Bounds removed!","color":"dark_red"}]
execute if entity @s[tag=mgs.element.boundary] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.boundary_corner_removed","fallback":"Boundary Corner removed!","color":"gray"}]
execute if entity @s[tag=mgs.element.search_and_destroy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.sd_demolition_removed","fallback":"S&D / Demolition removed!","color":"gold"}]
execute if entity @s[tag=mgs.element.domination] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.domination_point_removed","fallback":"Domination Point removed!","color":"green"}]
execute if entity @s[tag=mgs.element.hardpoint] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.hardpoint_zone_removed","fallback":"Hardpoint Zone removed!","color":"dark_purple"}]
execute if entity @s[tag=mgs.element.start_command] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.start_command_removed","fallback":"Start Command removed!","color":"aqua"}]
execute if entity @s[tag=mgs.element.respawn_command] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.respawn_command_removed","fallback":"Respawn Command removed!","color":"dark_aqua"}]
execute if entity @s[tag=mgs.element.mission_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.mission_spawn_removed","fallback":"Mission Spawn removed!","color":"aqua"}]
execute if entity @s[tag=mgs.element.enemy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.enemy_removed","fallback":"Enemy removed!","color":"red"}]
execute if entity @s[tag=mgs.element.zombie_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.zombie_spawn_removed","fallback":"Zombie Spawn removed!","color":"dark_green"}]
execute if entity @s[tag=mgs.element.player_spawn_zb] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.player_spawn_removed","fallback":"Player Spawn removed!","color":"aqua"}]
execute if entity @s[tag=mgs.element.special_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.special_spawn_removed","fallback":"Special Spawn removed!","color":"dark_red"}]
execute if entity @s[tag=mgs.element.wallbuy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.wallbuy_removed","fallback":"Wallbuy removed!","color":"yellow"}]
execute if entity @s[tag=mgs.element.door] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.door_removed","fallback":"Door removed!","color":"gold"}]
execute if entity @s[tag=mgs.element.trap] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.trap_removed","fallback":"Trap removed!","color":"red"}]
execute if entity @s[tag=mgs.element.perk_machine] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.perk_machine_removed","fallback":"Perk Machine removed!","color":"dark_purple"}]
execute if entity @s[tag=mgs.element.wunderfizz] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.der_wunderfizz_removed","fallback":"Der Wunderfizz removed!","color":"gold"}]
execute if entity @s[tag=mgs.element.pap_machine] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.pack_a_punch_removed","fallback":"Pack-a-Punch removed!","color":"dark_red"}]
execute if entity @s[tag=mgs.element.mystery_box_pos] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.mystery_box_pos_removed","fallback":"Mystery Box Pos removed!","color":"light_purple"}]
execute if entity @s[tag=mgs.element.power_switch] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.power_switch_removed","fallback":"Power Switch removed!","color":"green"}]
execute if entity @s[tag=mgs.element.barricade] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.barricade_removed","fallback":"Barricade removed!","color":"aqua"}]

# Elements with compound data (zb_object, enemy, spawn).
execute if data entity @s data run tellraw @a[tag=mgs.map_editor] ["  ",{"translate":"mgs.data","fallback":"Data: ","color":"gray"},{"entity":"@s","nbt":"data","color":"white"}]

kill @s

