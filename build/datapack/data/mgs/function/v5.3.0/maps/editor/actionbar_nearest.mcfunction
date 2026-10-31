
#> mgs:v5.3.0/maps/editor/actionbar_nearest
#
# @executed	as @n[type=minecraft:marker,tag=mgs.map_element,distance=..5]
#
# @within	mgs:v5.3.0/maps/editor/tick [ as @n[type=minecraft:marker,tag=mgs.map_element,distance=..5] ]
#

execute if entity @s[tag=mgs.element.base_coordinates] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"⬟ ","color":"light_purple"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.red_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"● ","color":"red"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.blue_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"● ","color":"blue"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.general_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"● ","color":"yellow"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.out_of_bounds] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"☠ ","color":"dark_red"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.boundary] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"◻ ","color":"gray"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.search_and_destroy] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"💣 ","color":"gold"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.domination] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🏴 ","color":"green"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.hardpoint] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"⚡ ","color":"dark_purple"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.start_command] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"⚙ ","color":"aqua"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.respawn_command] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"↺ ","color":"dark_aqua"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.mission_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"● ","color":"aqua"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.enemy] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"👤 ","color":"red"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.zombie_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🧟 ","color":"dark_green"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.player_spawn_zb] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"● ","color":"aqua"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.special_spawn] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🐺 ","color":"dark_red"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.wallbuy] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🔫 ","color":"yellow"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.door] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🚪 ","color":"gold"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.trap] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🔮 ","color":"red"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.perk_machine] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🧪 ","color":"dark_purple"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.wunderfizz] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🎰 ","color":"gold"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.pap_machine] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🔥 ","color":"dark_red"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.mystery_box_pos] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"📦 ","color":"light_purple"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.power_switch] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"⚡ ","color":"green"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.barricade] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🧱 ","color":"aqua"},{"selector":"@s"}]
execute if entity @s[tag=mgs.element.leaderboard] run return run title @a[tag=mgs.check_nearest] actionbar [{"text":"🏆 ","color":"gold"},{"selector":"@s"}]

