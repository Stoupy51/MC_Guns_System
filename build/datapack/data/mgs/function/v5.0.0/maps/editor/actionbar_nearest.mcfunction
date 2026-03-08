
#> mgs:v5.0.0/maps/editor/actionbar_nearest
#
# @executed	as @n[tag=mgs.map_element,distance=..5]
#
# @within	mgs:v5.0.0/maps/editor/tick [ as @n[tag=mgs.map_element,distance=..5] ]
#

execute if entity @s[tag=mgs.element.base_coordinates] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"⬟ ","color":"light_purple"},{"translate": "mgs.base_coordinates"}]
execute if entity @s[tag=mgs.element.red_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"● ","color":"red"},{"translate": "mgs.red_spawn"}]
execute if entity @s[tag=mgs.element.blue_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"● ","color":"blue"},{"translate": "mgs.blue_spawn"}]
execute if entity @s[tag=mgs.element.general_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"● ","color":"yellow"},{"translate": "mgs.general_spawn"}]
execute if entity @s[tag=mgs.element.out_of_bounds] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"☠ ","color":"dark_red"},{"translate": "mgs.out_of_bounds"}]
execute if entity @s[tag=mgs.element.boundary] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"◻ ","color":"gray"},{"translate": "mgs.boundary_corner"}]
execute if entity @s[tag=mgs.element.search_and_destroy] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"💣 ","color":"gold"},{"translate": "mgs.sd_objective"}]
execute if entity @s[tag=mgs.element.domination] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🏴 ","color":"green"},{"translate": "mgs.domination_point"}]
execute if entity @s[tag=mgs.element.hardpoint] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"⚡ ","color":"dark_purple"},{"translate": "mgs.hardpoint_zone"}]
execute if entity @s[tag=mgs.element.mission_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"● ","color":"aqua"},{"translate": "mgs.mission_spawn"}]
execute if entity @s[tag=mgs.element.enemy] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"👤 ","color":"red"},{"translate": "mgs.enemy"}]
execute if entity @s[tag=mgs.element.zombie_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🧟 ","color":"dark_green"},{"translate": "mgs.zombie_spawn"}]
execute if entity @s[tag=mgs.element.player_spawn_zb] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"● ","color":"aqua"},{"translate": "mgs.player_spawn"}]
execute if entity @s[tag=mgs.element.wallbuy] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🔫 ","color":"yellow"},{"translate": "mgs.wallbuy"}]
execute if entity @s[tag=mgs.element.door] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🚪 ","color":"gold"},{"translate": "mgs.door"}]
execute if entity @s[tag=mgs.element.trap] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"⚡ ","color":"red"},{"translate": "mgs.trap"}]
execute if entity @s[tag=mgs.element.perk_machine] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🧪 ","color":"dark_purple"},{"translate": "mgs.perk_machine"}]
execute if entity @s[tag=mgs.element.mystery_box_pos] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"📦 ","color":"light_purple"},{"translate": "mgs.mystery_box_pos"}]
execute if entity @s[tag=mgs.element.power_switch] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"⚡ ","color":"green"},{"translate": "mgs.power_switch"}]

