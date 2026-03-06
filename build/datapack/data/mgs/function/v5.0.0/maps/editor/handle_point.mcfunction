
#> mgs:v5.0.0/maps/editor/handle_point
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/process_element
#

# Get position for permanent marker
execute store result storage mgs:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage mgs:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage mgs:temp _pos.z double 1 run data get entity @s Pos[2]

# Determine tag
execute if entity @s[tag=mgs.element.out_of_bounds] run data modify storage mgs:temp _pos.tag set value "mgs.element.out_of_bounds"
execute if entity @s[tag=mgs.element.boundary] run data modify storage mgs:temp _pos.tag set value "mgs.element.boundary"
execute if entity @s[tag=mgs.element.search_and_destroy] run data modify storage mgs:temp _pos.tag set value "mgs.element.search_and_destroy"
execute if entity @s[tag=mgs.element.domination] run data modify storage mgs:temp _pos.tag set value "mgs.element.domination"
execute if entity @s[tag=mgs.element.hardpoint] run data modify storage mgs:temp _pos.tag set value "mgs.element.hardpoint"
execute if entity @s[tag=mgs.element.level_1_enemy] run data modify storage mgs:temp _pos.tag set value "mgs.element.level_1_enemy"
execute if entity @s[tag=mgs.element.level_2_enemy] run data modify storage mgs:temp _pos.tag set value "mgs.element.level_2_enemy"
execute if entity @s[tag=mgs.element.level_3_enemy] run data modify storage mgs:temp _pos.tag set value "mgs.element.level_3_enemy"
execute if entity @s[tag=mgs.element.level_4_enemy] run data modify storage mgs:temp _pos.tag set value "mgs.element.level_4_enemy"

# Summon permanent marker
function mgs:v5.0.0/maps/editor/summon_point_marker with storage mgs:temp _pos

# Announce
execute if entity @s[tag=mgs.element.out_of_bounds] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.out_of_bounds_placed","color":"dark_red"}]
execute if entity @s[tag=mgs.element.boundary] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.boundary_corner_placed","color":"gray"}]
execute if entity @s[tag=mgs.element.search_and_destroy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.sd_objective_placed","color":"gold"}]
execute if entity @s[tag=mgs.element.domination] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.domination_point_placed","color":"green"}]
execute if entity @s[tag=mgs.element.hardpoint] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.hardpoint_zone_placed","color":"dark_purple"}]
execute if entity @s[tag=mgs.element.level_1_enemy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.level_1_enemy_placed","color":"green"}]
execute if entity @s[tag=mgs.element.level_2_enemy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.level_2_enemy_placed","color":"yellow"}]
execute if entity @s[tag=mgs.element.level_3_enemy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.level_3_enemy_placed","color":"gold"}]
execute if entity @s[tag=mgs.element.level_4_enemy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.level_4_enemy_placed","color":"red"}]

