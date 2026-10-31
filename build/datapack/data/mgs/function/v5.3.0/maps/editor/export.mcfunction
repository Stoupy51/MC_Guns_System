
#> mgs:v5.3.0/maps/editor/export
#
# @within	string in mgs:v5.3.0/maps/editor/menu_entry_display {idx:$(idx),mode:$(mode)}
#
# @args		mode (unknown)
#			idx (unknown)
#

data modify storage mgs:temp dialog set value {"type": "minecraft:notice", "title": {"translate": "mgs.export_map","fallback": "Export Map", "color": "aqua", "bold": true}, "body": [{"type": "minecraft:plain_message", "width": 400, "contents": [[{"translate": "mgs.click_the_box_then_ctrla_and_ctrlc_to_import_the_map_paste_it_af","fallback": "Click the box, then Ctrl+A and Ctrl+C.\nTo import the map, paste it after", "color": "gray"}, "\n"], {"translate": "mgs.data","fallback": "data", "color": "yellow"}, {"text": " ", "color": "white"}, {"translate": "mgs.modify","fallback": "modify", "color": "yellow"}, {"text": " ", "color": "white"}, {"translate": "mgs.storage","fallback": "storage", "color": "yellow"}, {"text": " ", "color": "white"}, {"translate": "mgs_maps","fallback": "mgs:maps", "color": "green"}, {"text": " <", "color": "white"}, {"translate": "mgs.mode","fallback": "mode", "color": "yellow"}, {"text": "> ", "color": "white"}, {"translate": "mgs.append","fallback": "append", "color": "yellow"}, {"text": " ", "color": "white"}, {"translate": "mgs.value","fallback": "value", "color": "yellow"}, [{"text":"\n", "color": "gray"}, {"translate": "mgs.in_a_command_block_or_a_functionsince_chat_cuts_commands_at_256_","fallback": "in a command block or a function,\nsince chat cuts commands at 256 characters."}]]}], "inputs": [{"type": "minecraft:text", "key": "map", "label": "Map data", "initial": "", "max_length": 2000000, "width": 400, "multiline": {"max_lines": 512, "height": 200}}], "action": {"label": {"translate": "mgs.back","fallback": "Back", "color": "gray"}, "action": {"type": "run_command", "command": ""}}}
$data modify storage mgs:temp dialog.action.action.command set value "/function mgs:v5.3.0/maps/editor/list/$(mode)"
$data modify storage mgs:temp _export.map set from storage mgs:maps $(mode)[$(idx)]
scoreboard players set #export_ok mgs.data 0
execute store result score #export_ok mgs.data run function mgs:v5.3.0/maps/editor/export_text with storage mgs:temp _export
execute if score #export_ok mgs.data matches 1 run return run function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

# A text holding a double quote is printed in single quotes, which ends the one wrapping the macro value: chat and logs/latest.log get the map instead.
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.this_map_has_a_text_with_a_double_quote_so_it_is_printed_below_a","fallback":"This map has a text with a double quote, so it is printed below and in logs/latest.log instead.","color":"yellow"}]
tellraw @s {"storage":"mgs:temp","nbt":"_export.map","color":"white"}

