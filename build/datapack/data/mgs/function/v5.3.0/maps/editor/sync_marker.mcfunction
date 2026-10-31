
#> mgs:v5.3.0/maps/editor/sync_marker
#
# @executed	as @e[type=minecraft:marker,tag=mgs.map_element]
#
# @within	mgs:v5.3.0/maps/editor/global_tick [ as @e[type=minecraft:marker,tag=mgs.map_element] ]
#

data modify storage mgs:temp _ed_sig set value {}
data modify storage mgs:temp _ed_sig set from entity @s data
data remove storage mgs:temp _ed_sig._ed
data remove storage mgs:temp _ed_sig._disp_sig
execute store success score #ed_changed mgs.data run data modify entity @s data._ed.sig set from storage mgs:temp _ed_sig
execute if score #ed_changed mgs.data matches 1 run function mgs:v5.3.0/maps/editor/refresh_marker

