
#> mgs:v5.1.0/maps/editor/displays/snapshot
#
# @executed	as @e[type=minecraft:marker,tag=mgs.model_display]
#
# @within	mgs:v5.1.0/maps/editor/refresh_displays [ as @e[type=minecraft:marker,tag=mgs.model_display] ]
#			mgs:v5.1.0/maps/editor/displays/sync [ as @e[type=minecraft:marker,tag=mgs.model_display] ]
#

# @s = a model-display marker. Everything its display is built from is its data and position.
data modify storage mgs:temp _ed_sig set value {}
data modify storage mgs:temp _ed_sig.data set from entity @s data
data remove storage mgs:temp _ed_sig.data._disp_sig
data modify storage mgs:temp _ed_sig.pos set from entity @s Pos
execute store success score #ed_sig_changed mgs.data run data modify entity @s data._disp_sig set from storage mgs:temp _ed_sig
execute if score #ed_sig_changed mgs.data matches 1 run scoreboard players set #ed_disp_dirty mgs.data 1

