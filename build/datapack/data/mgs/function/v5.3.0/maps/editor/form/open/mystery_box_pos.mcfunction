
#> mgs:v5.3.0/maps/editor/form/open/mystery_box_pos
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.3.0/maps/editor/show_element_config
#

function mgs:v5.3.0/maps/editor/form/target
data modify storage mgs:temp dialog set value {"type": "minecraft:multi_action", "title": {"translate": "mgs.mystery_box","fallback": "Mystery Box", "color": "light_purple", "bold": true}, "body": [{"type": "minecraft:plain_message", "width": 400, "contents": [{"translate": "mgs.the_box_turns_about_the_centre_of_its_block_upside_down_it_hangs","fallback": "The box turns about the centre of its block.\nUpside down, it hangs from the block above.", "color": "gray"}]}, {"type": "minecraft:plain_message", "width": 400, "contents": ["", {"translate": "mgs.hover_a_name_for_its_help","fallback": "Hover a name for its help:", "color": "gray"}, "\n", [{"text":"ⓘ ", "color": "aqua", "hover_event": {"action": "show_text", "value": [{"text": "Tilt of the box, ", "color": "gray"}, {"text": "-90", "color": "green"}, {"text": " to ", "color": "gray"}, {"text": "90", "color": "green"}, {"text": "\ndegrees. Every animation follows\nthe box's own up.", "color": "gray"}]}}, {"translate": "mgs.pitch","fallback": "Pitch"}], "   ", [{"text":"ⓘ ", "color": "aqua", "hover_event": {"action": "show_text", "value": [{"text": "Turn about its front axis:\n", "color": "gray"}, {"text": "0", "color": "green"}, {"text": ", ", "color": "gray"}, {"text": "90", "color": "green"}, {"text": ", ", "color": "gray"}, {"text": "180", "color": "green"}, {"text": " or ", "color": "gray"}, {"text": "270", "color": "green"}, {"text": ".\n", "color": "gray"}, {"text": "180", "color": "green"}, {"text": ": upside down, for a ceiling.", "color": "gray"}]}}, {"translate": "mgs.roll","fallback": "Roll"}], "   ", [{"text":"ⓘ ", "color": "aqua", "hover_event": {"action": "show_text", "value": [{"text": "true", "color": "green"}, {"text": ": it may be the first spot.\n", "color": "gray"}, {"text": "false", "color": "green"}, {"text": ": only reached by moving.\nOnly one spot is active at once;\nthe others show a grayed model.\nAt least one spot must allow it.", "color": "gray"}]}}, {"translate": "mgs.first_spot","fallback": "First spot"}], "   ", [{"text":"ⓘ ", "color": "aqua", "hover_event": {"action": "show_text", "value": [{"text": "Announced in chat when the box\nlands here: ", "color": "gray"}, {"text": "\"the Power Room\"", "color": "green"}, {"text": ".\nEmpty: a generic message.", "color": "gray"}]}}, {"translate": "mgs.location_name","fallback": "Location name"}]]}], "inputs": [{"type": "minecraft:number_range", "key": "yaw", "label": "Yaw", "start": 0, "end": 359, "step": 1, "width": 300}, {"type": "minecraft:number_range", "key": "pitch", "label": "Pitch", "start": -90, "end": 90, "step": 1, "width": 300}, {"type": "minecraft:single_option", "key": "roll", "label": "Roll", "width": 300, "options": [{"id": "0", "display": "0"}, {"id": "90", "display": "90"}, {"id": "180", "display": "180 (upside down)"}, {"id": "270", "display": "270"}]}, {"type": "minecraft:boolean", "key": "can_start_on", "label": "Can be the first spot", "initial": true, "on_true": "1", "on_false": "0"}, {"type": "minecraft:text", "key": "location_name", "label": {"translate": "mgs.location_name","fallback": "Location name", "hover_event": {"action": "show_text", "value": [{"translate": "mgs.announced_in_chat_when_the_boxlands_here","fallback": "Announced in chat when the box\nlands here: ", "color": "gray"}, {"translate": "mgs.the_power_room","fallback": "\"the Power Room\"", "color": "green"}, [{"text":".\n", "color": "gray"}, {"translate": "mgs.empty_a_generic_message","fallback": "Empty: a generic message."}]]}}, "initial": "", "max_length": 64, "width": 300}], "actions": [{"label": {"translate": "mgs.save","fallback": "Save", "color": "green"}, "action": {"type": "dynamic/run_command", "template": "/function mgs:v5.3.0/maps/editor/form/mystery_box_apply {yaw:$(yaw),pitch:$(pitch),roll:$(roll),can_start_on:$(can_start_on),location_name:\"$(location_name)\"}"}}], "exit_action": {"label": {"translate": "mgs.cancel","fallback": "Cancel", "color": "gray"}}}

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

