
#> mgs:v5.1.0/maps/editor/particles
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/maps/editor/global_tick
#

# Rotation indicator, skipped for markers that already draw a real model
execute as @e[type=minecraft:marker,tag=mgs.map_element,tag=!mgs.element.wallbuy,tag=!mgs.element.perk_machine,tag=!mgs.element.pap_machine,tag=!mgs.element.mystery_box_pos,tag=!mgs.element.power_switch,tag=!mgs.element.barrier] at @s positioned ^ ^ ^0.5 run particle dust{color:[1.0,1.0,1.0],scale:0.5} ~ ~1.69 ~ 0.1 0.1 0.1 0 5 normal @a[scores={mgs.mp.map_edit=1},distance=..48]

# Per-element markers
execute at @e[tag=mgs.element.base_coordinates] run particle dust{color:[1.0,0.0,1.0],scale:1.5} ~ ~1 ~ 0.3 0.5 0.3 0 2 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.red_spawn] run particle dust{color:[1.0,0.2,0.2],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.blue_spawn] run particle dust{color:[0.2,0.2,1.0],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.general_spawn] run particle dust{color:[1.0,1.0,0.2],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.out_of_bounds] run particle dust{color:[0.6,0.0,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.boundary] run particle dust{color:[0.8,0.8,0.8],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.search_and_destroy] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.domination] run particle dust{color:[0.0,1.0,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.hardpoint] run particle dust{color:[0.5,0.0,0.5],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.start_command] run particle dust{color:[0.0,0.9,0.9],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.respawn_command] run particle dust{color:[0.0,0.7,0.7],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.mission_spawn] run particle dust{color:[0.0,1.0,1.0],scale:1.0} ~ ~1 ~ 0.2 0.5 0.2 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.enemy] run particle dust{color:[1.0,0.2,0.2],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.zombie_spawn] run particle dust{color:[0.0,0.5,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.player_spawn_zb] run particle dust{color:[0.0,1.0,1.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.special_spawn] run particle dust{color:[0.6,0.0,0.2],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.door] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]
execute at @e[tag=mgs.element.trap] run particle dust{color:[1.0,0.2,0.2],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[scores={mgs.mp.map_edit=1},distance=..48]

