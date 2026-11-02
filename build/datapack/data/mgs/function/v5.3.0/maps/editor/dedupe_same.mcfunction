
#> mgs:v5.3.0/maps/editor/dedupe_same
#
# @executed	as @e[type=minecraft:marker,tag=...,distance=..0.01]
#
# @within	mgs:v5.3.0/maps/editor/dedupe/red_spawn [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/blue_spawn [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/general_spawn [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/out_of_bounds [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/boundary [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/search_and_destroy [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/domination [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/hardpoint [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/start_command [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/respawn_command [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/mission_spawn [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/enemy [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/zombie_spawn [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/player_spawn_zb [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/special_spawn [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/wallbuy [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/door [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/trap [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/perk_machine [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/wunderfizz [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/pap_machine [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/mystery_box_pos [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/power_switch [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#			mgs:v5.3.0/maps/editor/dedupe/barricade [ as @e[type=minecraft:marker,tag=...,distance=..0.01] ]
#

data modify storage mgs:temp _dedupe_other set from entity @s data
data remove storage mgs:temp _dedupe_other._ed
data remove storage mgs:temp _dedupe_other._disp_sig
execute store success score #differs mgs.data run data modify storage mgs:temp _dedupe_other set from storage mgs:temp _dedupe
execute if score #differs mgs.data matches 0 run tag @s add mgs.ed_dup

