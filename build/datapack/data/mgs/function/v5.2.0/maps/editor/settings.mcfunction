
#> mgs:v5.2.0/maps/editor/settings
#
# @within	string in mgs:v5.2.0/maps/editor/menu_entry_display {idx:$(idx),mode:$(mode)}
#
# @args		mode (unknown)
#			idx (unknown)
#

$data modify storage mgs:temp map_settings.target set value {mode:"$(mode)",idx:$(idx)}
data modify storage mgs:temp dialog set value {"type": "minecraft:confirmation", "title": {"translate": "mgs.map_settings","fallback": "Map Settings", "color": "gold", "bold": true}, "body": [{"type": "minecraft:plain_message", "contents": {"translate": "mgs.dimension_minecraft_overworld_mgs_zombies_minecraft_the_nether_m","fallback": "Dimension: minecraft:overworld, mgs:zombies, minecraft:the_nether, minecraft:the_end or any other.", "color": "gray"}}], "inputs": [{"type": "minecraft:text", "key": "name", "label": "Name", "initial": "", "max_length": 64, "width": 300}, {"type": "minecraft:text", "key": "description", "label": "Description", "initial": "", "max_length": 256, "width": 300}, {"type": "minecraft:text", "key": "dimension", "label": "Dimension", "initial": "minecraft:overworld", "max_length": 128, "width": 300}], "yes": {"label": {"translate": "mgs.save","fallback": "Save", "color": "green"}, "action": {"type": "dynamic/run_command", "template": "/function mgs:v5.2.0/maps/editor/settings_apply {name:\"$(name)\",description:\"$(description)\",dimension:\"$(dimension)\"}"}}, "no": {"label": {"translate": "mgs.cancel","fallback": "Cancel", "color": "red"}, "action": {"type": "run_command", "command": ""}}}
$data modify storage mgs:temp dialog.inputs[0].initial set from storage mgs:maps $(mode)[$(idx)].name
$data modify storage mgs:temp dialog.inputs[1].initial set from storage mgs:maps $(mode)[$(idx)].description
$data modify storage mgs:temp dialog.inputs[2].initial set from storage mgs:maps $(mode)[$(idx)].dimension
$data modify storage mgs:temp dialog.no.action.command set value "/function mgs:v5.2.0/maps/editor/list/$(mode)"
function mgs:v5.2.0/multiplayer/show_dialog with storage mgs:temp

