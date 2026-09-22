
#> mgs:v5.1.0/maps/editor/refresh_displays
#
# @within	mgs:v5.1.0/maps/editor/enter
#			mgs:v5.1.0/maps/editor/handle_zb_object
#			mgs:v5.1.0/maps/editor/handle_destroy
#			mgs:v5.1.0/maps/editor/displays/sync
#

# Rebuild all editor model displays from the current markers
kill @e[tag=mgs.editor_display]
execute as @e[type=minecraft:marker,tag=mgs.element.wallbuy] at @s run function mgs:v5.1.0/maps/editor/displays/wallbuy
execute as @e[type=minecraft:marker,tag=mgs.element.perk_machine] at @s run function mgs:v5.1.0/maps/editor/displays/perk_machine
execute as @e[type=minecraft:marker,tag=mgs.element.wunderfizz] at @s run function mgs:v5.1.0/maps/editor/displays/wunderfizz
execute as @e[type=minecraft:marker,tag=mgs.element.pap_machine] at @s run function mgs:v5.1.0/maps/editor/displays/pap_machine
execute as @e[type=minecraft:marker,tag=mgs.element.mystery_box_pos] at @s run function mgs:v5.1.0/maps/editor/displays/mystery_box_pos
execute as @e[type=minecraft:marker,tag=mgs.element.power_switch] at @s run function mgs:v5.1.0/maps/editor/displays/power_switch
execute as @e[type=minecraft:marker,tag=mgs.element.barricade] at @s run function mgs:v5.1.0/maps/editor/displays/barricade

# Snapshot what was just drawn, so displays/sync only rebuilds after a real edit
tag @e[type=minecraft:marker,tag=mgs.element.wallbuy] add mgs.model_display
tag @e[type=minecraft:marker,tag=mgs.element.perk_machine] add mgs.model_display
tag @e[type=minecraft:marker,tag=mgs.element.wunderfizz] add mgs.model_display
tag @e[type=minecraft:marker,tag=mgs.element.pap_machine] add mgs.model_display
tag @e[type=minecraft:marker,tag=mgs.element.mystery_box_pos] add mgs.model_display
tag @e[type=minecraft:marker,tag=mgs.element.power_switch] add mgs.model_display
tag @e[type=minecraft:marker,tag=mgs.element.barricade] add mgs.model_display
execute as @e[type=minecraft:marker,tag=mgs.model_display] run function mgs:v5.1.0/maps/editor/displays/snapshot
execute store result score #ed_disp_count mgs.data if entity @e[type=minecraft:marker,tag=mgs.model_display]

