
#> mgs:v5.3.0/maps/editor/revert_marker
#
# @within	mgs:v5.3.0/maps/editor/revert
#

data modify entity @s {} merge from storage mgs:temp _ed_revert

# Another form may target its own marker since.
tag @s remove mgs.ed_form_target
function mgs:v5.3.0/maps/editor/sync_marker
execute if entity @s[tag=mgs.element.base_coordinates] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.base_coordinates_restored","fallback":"Base Coordinates restored!","color":"light_purple"}]
execute if entity @s[tag=mgs.element.red_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red_spawn_restored","fallback":"Red Spawn restored!","color":"red"}]
execute if entity @s[tag=mgs.element.blue_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.blue_spawn_restored","fallback":"Blue Spawn restored!","color":"blue"}]
execute if entity @s[tag=mgs.element.general_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.general_spawn_restored","fallback":"General Spawn restored!","color":"yellow"}]
execute if entity @s[tag=mgs.element.out_of_bounds] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.out_of_bounds_restored","fallback":"Out of Bounds restored!","color":"dark_red"}]
execute if entity @s[tag=mgs.element.boundary] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.boundary_corner_restored","fallback":"Boundary Corner restored!","color":"gray"}]
execute if entity @s[tag=mgs.element.search_and_destroy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.sd_demolition_restored","fallback":"S&D / Demolition restored!","color":"gold"}]
execute if entity @s[tag=mgs.element.domination] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.domination_point_restored","fallback":"Domination Point restored!","color":"green"}]
execute if entity @s[tag=mgs.element.hardpoint] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.hardpoint_zone_restored","fallback":"Hardpoint Zone restored!","color":"dark_purple"}]
execute if entity @s[tag=mgs.element.start_command] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.start_command_restored","fallback":"Start Command restored!","color":"aqua"}]
execute if entity @s[tag=mgs.element.respawn_command] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.respawn_command_restored","fallback":"Respawn Command restored!","color":"dark_aqua"}]
execute if entity @s[tag=mgs.element.mission_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.mission_spawn_restored","fallback":"Mission Spawn restored!","color":"aqua"}]
execute if entity @s[tag=mgs.element.enemy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.enemy_restored","fallback":"Enemy restored!","color":"red"}]
execute if entity @s[tag=mgs.element.zombie_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.zombie_spawn_restored","fallback":"Zombie Spawn restored!","color":"dark_green"}]
execute if entity @s[tag=mgs.element.player_spawn_zb] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.player_spawn_restored","fallback":"Player Spawn restored!","color":"aqua"}]
execute if entity @s[tag=mgs.element.special_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.special_spawn_restored","fallback":"Special Spawn restored!","color":"dark_red"}]
execute if entity @s[tag=mgs.element.wallbuy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.wallbuy_restored","fallback":"Wallbuy restored!","color":"yellow"}]
execute if entity @s[tag=mgs.element.door] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.door_restored","fallback":"Door restored!","color":"gold"}]
execute if entity @s[tag=mgs.element.trap] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.trap_restored","fallback":"Trap restored!","color":"red"}]
execute if entity @s[tag=mgs.element.perk_machine] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.perk_machine_restored","fallback":"Perk Machine restored!","color":"dark_purple"}]
execute if entity @s[tag=mgs.element.wunderfizz] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.der_wunderfizz_restored","fallback":"Der Wunderfizz restored!","color":"gold"}]
execute if entity @s[tag=mgs.element.pap_machine] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.pack_a_punch_restored","fallback":"Pack-a-Punch restored!","color":"dark_red"}]
execute if entity @s[tag=mgs.element.mystery_box_pos] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.mystery_box_pos_restored","fallback":"Mystery Box Pos restored!","color":"light_purple"}]
execute if entity @s[tag=mgs.element.power_switch] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.power_switch_restored","fallback":"Power Switch restored!","color":"green"}]
execute if entity @s[tag=mgs.element.barricade] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.barricade_restored","fallback":"Barricade restored!","color":"aqua"}]
execute if entity @s[tag=mgs.element.leaderboard] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.leaderboard_restored","fallback":"Leaderboard restored!","color":"gold"}]

