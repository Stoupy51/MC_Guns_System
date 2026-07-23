
#> mgs:v5.1.0/maps/editor/displays/wunderfizz
#
# @executed	as @e[tag=mgs.element.wunderfizz] & at @s
#
# @within	mgs:v5.1.0/maps/editor/refresh_displays [ as @e[tag=mgs.element.wunderfizz] & at @s ]
#

# @s = wunderfizz marker, at @s
data modify storage mgs:temp _wf_disp.tag set value "mgs.editor_display"
data modify storage mgs:temp _wf_disp.item_id set value ""
data modify storage mgs:temp _wf_disp.item_model set value ""
data modify storage mgs:temp _wf_disp.yaw set value 0.0f
execute if data entity @s data.display_item run data modify storage mgs:temp _wf_disp.item_id set from entity @s data.display_item
execute if data entity @s data.item_model run data modify storage mgs:temp _wf_disp.item_model set from entity @s data.item_model
execute if data storage mgs:temp _wf_disp{item_id:""} run data modify storage mgs:temp _wf_disp.item_id set value "minecraft:potion"
execute if data storage mgs:temp _wf_disp{item_model:""} run data modify storage mgs:temp _wf_disp.item_model set value "mgs:der_wunderfizz"
execute if data entity @s data.yaw run data modify storage mgs:temp _wf_disp.yaw set from entity @s data.yaw
execute align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function mgs:v5.1.0/zombies/display/summon_machine_display with storage mgs:temp _wf_disp

