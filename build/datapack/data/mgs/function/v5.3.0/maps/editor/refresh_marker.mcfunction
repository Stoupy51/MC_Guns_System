
#> mgs:v5.3.0/maps/editor/refresh_marker
#
# @executed	as @e[type=minecraft:marker,tag=mgs.map_element]
#
# @within	mgs:v5.3.0/maps/editor/sync_marker
#

execute if data entity @s data.yaw run data modify entity @s Rotation[0] set from entity @s data.yaw
execute if entity @s[tag=mgs.element.zombie_spawn] run function mgs:v5.3.0/maps/editor/spawn_shapes
execute if entity @s[tag=mgs.element.special_spawn] run function mgs:v5.3.0/maps/editor/spawn_shapes

# The data, plus what a name shows that is not plain data.
data modify storage mgs:temp _ed_name set value {group:"",rounds:"",entity:"",arrival_flag:"",power_flag:""}
data modify storage mgs:temp _ed_name merge from entity @s data
execute if data entity @s data.group_id run function mgs:v5.3.0/maps/editor/name/group with entity @s data
execute if data entity @s data.min_round run function mgs:v5.3.0/maps/editor/name/rounds
execute if data entity @s data.mob.entity run function mgs:v5.3.0/maps/editor/name/entity
execute if data entity @s data{power:1b} run data modify storage mgs:temp _ed_name.power_flag set value " power"
execute if entity @s[tag=mgs.element.base_coordinates] run return run function mgs:v5.3.0/maps/editor/name/base_coordinates
execute if entity @s[tag=mgs.element.red_spawn] run return run function mgs:v5.3.0/maps/editor/name/red_spawn
execute if entity @s[tag=mgs.element.blue_spawn] run return run function mgs:v5.3.0/maps/editor/name/blue_spawn
execute if entity @s[tag=mgs.element.general_spawn] run return run function mgs:v5.3.0/maps/editor/name/general_spawn
execute if entity @s[tag=mgs.element.out_of_bounds] run return run function mgs:v5.3.0/maps/editor/name/out_of_bounds
execute if entity @s[tag=mgs.element.boundary] run return run function mgs:v5.3.0/maps/editor/name/boundary
execute if entity @s[tag=mgs.element.search_and_destroy] run return run function mgs:v5.3.0/maps/editor/name/search_and_destroy
execute if entity @s[tag=mgs.element.domination] run return run function mgs:v5.3.0/maps/editor/name/domination
execute if entity @s[tag=mgs.element.hardpoint] run return run function mgs:v5.3.0/maps/editor/name/hardpoint
execute if entity @s[tag=mgs.element.start_command] run return run function mgs:v5.3.0/maps/editor/name/start_command
execute if entity @s[tag=mgs.element.respawn_command] run return run function mgs:v5.3.0/maps/editor/name/respawn_command
execute if entity @s[tag=mgs.element.mission_spawn] run return run function mgs:v5.3.0/maps/editor/name/mission_spawn
execute if entity @s[tag=mgs.element.enemy] run return run function mgs:v5.3.0/maps/editor/name/enemy
execute if entity @s[tag=mgs.element.config] run return run function mgs:v5.3.0/maps/editor/name/config
execute if entity @s[tag=mgs.element.zombie_spawn] run return run function mgs:v5.3.0/maps/editor/name/zombie_spawn
execute if entity @s[tag=mgs.element.player_spawn_zb] run return run function mgs:v5.3.0/maps/editor/name/player_spawn_zb
execute if entity @s[tag=mgs.element.special_spawn] run return run function mgs:v5.3.0/maps/editor/name/special_spawn
execute if entity @s[tag=mgs.element.wallbuy] run return run function mgs:v5.3.0/maps/editor/name/wallbuy
execute if entity @s[tag=mgs.element.door] run return run function mgs:v5.3.0/maps/editor/name/door
execute if entity @s[tag=mgs.element.trap] run return run function mgs:v5.3.0/maps/editor/name/trap
execute if entity @s[tag=mgs.element.perk_machine] run return run function mgs:v5.3.0/maps/editor/name/perk_machine
execute if entity @s[tag=mgs.element.wunderfizz] run return run function mgs:v5.3.0/maps/editor/name/wunderfizz
execute if entity @s[tag=mgs.element.pap_machine] run return run function mgs:v5.3.0/maps/editor/name/pap_machine
execute if entity @s[tag=mgs.element.mystery_box_pos] run return run function mgs:v5.3.0/maps/editor/name/mystery_box_pos
execute if entity @s[tag=mgs.element.power_switch] run return run function mgs:v5.3.0/maps/editor/name/power_switch
execute if entity @s[tag=mgs.element.barricade] run return run function mgs:v5.3.0/maps/editor/name/barricade

