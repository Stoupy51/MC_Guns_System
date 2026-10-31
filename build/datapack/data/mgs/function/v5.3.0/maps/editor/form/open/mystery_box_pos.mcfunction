
#> mgs:v5.3.0/maps/editor/form/open/mystery_box_pos
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.3.0/maps/editor/show_element_config
#

function mgs:v5.3.0/maps/editor/form/target
data modify storage mgs:temp dialog set value {"type": "minecraft:multi_action", "title": {"translate": "mgs.mystery_box","fallback": "Mystery Box", "color": "light_purple", "bold": true}, "body": [{"type": "minecraft:plain_message", "width": 400, "contents": "The box turns about the centre of the block it was placed in: upside down, it hangs from the block above. Every animation follows its own up."}], "inputs": [{"type": "minecraft:number_range", "key": "yaw", "label": "Yaw", "start": 0, "end": 359, "step": 1, "width": 300}, {"type": "minecraft:number_range", "key": "pitch", "label": "Pitch", "start": -90, "end": 90, "step": 1, "width": 300}, {"type": "minecraft:single_option", "key": "roll", "label": "Roll", "width": 300, "options": [{"id": "0", "display": "0"}, {"id": "90", "display": "90"}, {"id": "180", "display": "180 (upside down)"}, {"id": "270", "display": "270"}]}, {"type": "minecraft:boolean", "key": "can_start_on", "label": "Can be the first spot", "initial": true, "on_true": "1", "on_false": "0"}, {"type": "minecraft:text", "key": "location_name", "label": "Location name, announced when the box lands here", "initial": "", "max_length": 64, "width": 300}], "actions": [{"label": {"translate": "mgs.save","fallback": "Save", "color": "green"}, "action": {"type": "dynamic/run_command", "template": "/function mgs:v5.3.0/maps/editor/form/mystery_box_apply {yaw:$(yaw),pitch:$(pitch),roll:$(roll),can_start_on:$(can_start_on),location_name:\"$(location_name)\"}"}}], "exit_action": {"label": {"translate": "mgs.cancel","fallback": "Cancel", "color": "gray"}}}

execute store result score #ed_v mgs.data run data get entity @s data.yaw
scoreboard players operation #ed_v mgs.data %= #360 mgs.data
execute store result storage mgs:temp dialog.inputs[0].initial float 1 run scoreboard players get #ed_v mgs.data
execute store result score #ed_v mgs.data run data get entity @s data.pitch
execute if score #ed_v mgs.data matches ..-91 run scoreboard players set #ed_v mgs.data -90
execute if score #ed_v mgs.data matches 91.. run scoreboard players set #ed_v mgs.data 90
execute store result storage mgs:temp dialog.inputs[1].initial float 1 run scoreboard players get #ed_v mgs.data
execute store result score #ed_v mgs.data run data get entity @s data.roll
scoreboard players operation #ed_v mgs.data /= #90 mgs.data
scoreboard players operation #ed_v mgs.data %= #4 mgs.data
execute if score #ed_v mgs.data matches 0 run data modify storage mgs:temp dialog.inputs[2].options[0].initial set value 1b
execute if score #ed_v mgs.data matches 1 run data modify storage mgs:temp dialog.inputs[2].options[1].initial set value 1b
execute if score #ed_v mgs.data matches 2 run data modify storage mgs:temp dialog.inputs[2].options[2].initial set value 1b
execute if score #ed_v mgs.data matches 3 run data modify storage mgs:temp dialog.inputs[2].options[3].initial set value 1b
data modify storage mgs:temp dialog.inputs[3].initial set from entity @s data.can_start_on
data modify storage mgs:temp dialog.inputs[4].initial set from entity @s data.location_name
execute as @a[tag=mgs.ed_form_user] run function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

