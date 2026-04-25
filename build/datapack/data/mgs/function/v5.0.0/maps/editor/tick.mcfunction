
#> mgs:v5.0.0/maps/editor/tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Only run for players in editor mode
execute unless score @s mgs.mp.map_edit matches 1 run return fail

# Show rotation indicator for all markers
execute as @e[tag=mgs.map_element] run data modify entity @s Rotation[0] set from entity @s data.yaw
execute as @e[tag=mgs.map_element] at @s positioned ^ ^ ^0.5 run particle dust{color:[1.0,1.0,1.0],scale:0.5} ~ ~1.69 ~ 0.1 0.1 0.1 0 5

# Per-element particles
execute at @e[tag=mgs.element.base_coordinates] run particle dust{color:[1.0,0.0,1.0],scale:1.5} ~ ~1 ~ 0.3 0.5 0.3 0 2
execute at @e[tag=mgs.element.red_spawn] run particle dust{color:[1.0,0.2,0.2],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 1
execute at @e[tag=mgs.element.blue_spawn] run particle dust{color:[0.2,0.2,1.0],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 1
execute at @e[tag=mgs.element.general_spawn] run particle dust{color:[1.0,1.0,0.2],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 1
execute at @e[tag=mgs.element.out_of_bounds] run particle dust{color:[0.6,0.0,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.boundary] run particle dust{color:[0.8,0.8,0.8],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.search_and_destroy] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.domination] run particle dust{color:[0.0,1.0,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.hardpoint] run particle dust{color:[0.5,0.0,0.5],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.start_command] run particle dust{color:[0.0,0.9,0.9],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.respawn_command] run particle dust{color:[0.0,0.7,0.7],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.mission_spawn] run particle dust{color:[0.0,1.0,1.0],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 1
execute at @e[tag=mgs.element.enemy] run particle dust{color:[1.0,0.2,0.2],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.zombie_spawn] run particle dust{color:[0.0,0.5,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.player_spawn_zb] run particle dust{color:[0.0,1.0,1.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.wallbuy] run particle dust{color:[1.0,1.0,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.door] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.trap] run particle dust{color:[1.0,0.2,0.2],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.perk_machine] run particle dust{color:[0.5,0.0,0.5],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.pap_machine] run particle dust{color:[0.8,0.1,0.1],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.mystery_box_pos] run particle dust{color:[1.0,0.0,1.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.power_switch] run particle dust{color:[0.0,1.0,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1
execute at @e[tag=mgs.element.barrier] run particle dust{color:[0.0,1.0,1.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1

# Actionbar: show nearest element info (within 5 blocks)
tag @s add mgs.check_nearest
execute as @n[tag=mgs.map_element,distance=..5] run function mgs:v5.0.0/maps/editor/actionbar_nearest
tag @s remove mgs.check_nearest

