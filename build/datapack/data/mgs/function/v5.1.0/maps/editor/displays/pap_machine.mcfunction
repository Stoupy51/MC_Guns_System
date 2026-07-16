
#> mgs:v5.1.0/maps/editor/displays/pap_machine
#
# @executed	at @s
#
# @within	mgs:v5.1.0/maps/editor/refresh_displays [ at @s ]
#

# @s = pap machine marker, at @s
data modify storage mgs:temp _pap_disp.tag set value "mgs.editor_display"
data modify storage mgs:temp _pap_disp.item_id set value ""
data modify storage mgs:temp _pap_disp.item_model set value ""
data modify storage mgs:temp _pap_disp.yaw set value 0.0f
execute if data entity @s data.display_item run data modify storage mgs:temp _pap_disp.item_id set from entity @s data.display_item
execute if data entity @s data.item_model run data modify storage mgs:temp _pap_disp.item_model set from entity @s data.item_model
execute if data storage mgs:temp _pap_disp{item_id:""} run data modify storage mgs:temp _pap_disp.item_id set value "minecraft:netherite_block"
execute if data storage mgs:temp _pap_disp{item_model:""} run data modify storage mgs:temp _pap_disp.item_model set value "mgs:pack_a_punch"
execute if data entity @s data.yaw run data modify storage mgs:temp _pap_disp.yaw set from entity @s data.yaw
execute positioned ^ ^ ^-0.5 positioned ~ ~-0.4 ~ run function mgs:v5.1.0/zombies/display/summon_machine_display with storage mgs:temp _pap_disp

