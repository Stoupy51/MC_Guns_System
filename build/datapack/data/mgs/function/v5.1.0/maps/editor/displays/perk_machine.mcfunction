
#> mgs:v5.1.0/maps/editor/displays/perk_machine
#
# @executed	at @s
#
# @within	mgs:v5.1.0/maps/editor/refresh_displays [ at @s ]
#

# @s = perk machine marker, at @s
data modify storage mgs:temp _pk_disp.tag set value "mgs.editor_display"
data modify storage mgs:temp _pk_disp.item_id set value ""
data modify storage mgs:temp _pk_disp.item_model set value ""
data modify storage mgs:temp _pk_disp.yaw set value 0.0f
execute if data entity @s data.display_item run data modify storage mgs:temp _pk_disp.item_id set from entity @s data.display_item
execute if data entity @s data.item_model run data modify storage mgs:temp _pk_disp.item_model set from entity @s data.item_model
execute if data storage mgs:temp _pk_disp{item_id:""} run data modify storage mgs:temp _pk_disp.item_id set value "minecraft:potion"
execute if data storage mgs:temp _pk_disp{item_model:""} run data modify storage mgs:temp _pk_disp.item_model set value "minecraft:potion"
data modify storage mgs:temp _pk_disp.perk_id set from entity @s data.perk_id
execute if data storage mgs:temp _pk_disp{item_model:"minecraft:potion"} run function mgs:v5.1.0/zombies/perks/override_perk_model with storage mgs:temp _pk_disp
execute if data entity @s data.yaw run data modify storage mgs:temp _pk_disp.yaw set from entity @s data.yaw
execute align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function mgs:v5.1.0/zombies/display/summon_machine_display with storage mgs:temp _pk_disp

