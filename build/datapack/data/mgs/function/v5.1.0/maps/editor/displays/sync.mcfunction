
#> mgs:v5.1.0/maps/editor/displays/sync
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/maps/editor/global_tick
#

scoreboard players set #ed_disp_dirty mgs.data 0
execute as @e[type=minecraft:marker,tag=mgs.model_display] run function mgs:v5.1.0/maps/editor/displays/snapshot
execute store result score #ed_disp_now mgs.data if entity @e[type=minecraft:marker,tag=mgs.model_display]
execute unless score #ed_disp_now mgs.data = #ed_disp_count mgs.data run scoreboard players set #ed_disp_dirty mgs.data 1
execute if score #ed_disp_dirty mgs.data matches 1 run function mgs:v5.1.0/maps/editor/refresh_displays

