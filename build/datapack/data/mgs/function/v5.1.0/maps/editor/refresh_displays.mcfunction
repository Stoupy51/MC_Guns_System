
#> mgs:v5.1.0/maps/editor/refresh_displays
#
# @within	mgs:v5.1.0/maps/editor/enter
#			mgs:v5.1.0/maps/editor/handle_zb_object
#			mgs:v5.1.0/maps/editor/handle_destroy
#			mgs:v5.1.0/maps/editor/global_tick
#

# Rebuild all editor model displays from the current markers
kill @e[tag=mgs.editor_display]
execute as @e[tag=mgs.element.wallbuy] at @s run function mgs:v5.1.0/maps/editor/displays/wallbuy
execute as @e[tag=mgs.element.perk_machine] at @s run function mgs:v5.1.0/maps/editor/displays/perk_machine
execute as @e[tag=mgs.element.pap_machine] at @s run function mgs:v5.1.0/maps/editor/displays/pap_machine
execute as @e[tag=mgs.element.mystery_box_pos] at @s run function mgs:v5.1.0/maps/editor/displays/mystery_box_pos
execute as @e[tag=mgs.element.power_switch] at @s run function mgs:v5.1.0/maps/editor/displays/power_switch
execute as @e[tag=mgs.element.barrier] at @s run function mgs:v5.1.0/maps/editor/displays/barrier

