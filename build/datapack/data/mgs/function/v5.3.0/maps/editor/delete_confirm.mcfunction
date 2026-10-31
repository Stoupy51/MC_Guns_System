
#> mgs:v5.3.0/maps/editor/delete_confirm
#
# @within	string in mgs:v5.3.0/maps/editor/menu_entry_display {idx:$(idx),mode:$(mode)}
#
# @args		mode (unknown)
#			idx (unknown)
#

data modify storage mgs:temp dialog set value {"type": "minecraft:confirmation", "title": {"translate": "mgs.delete_map","fallback": "Delete Map", "color": "red", "bold": true}, "body": [{"type": "minecraft:plain_message", "contents": [{"translate": "mgs.delete_2","fallback": "Delete "}, {"text": "", "color": "gold"}, [{"text":"?\n"}, {"translate": "mgs.this_cannot_be_undone","fallback": "This cannot be undone."}]]}], "yes": {"label": {"translate": "mgs.delete","fallback": "Delete", "color": "red"}, "action": {"type": "run_command", "command": ""}}, "no": {"label": {"translate": "mgs.cancel","fallback": "Cancel", "color": "gray"}, "action": {"type": "run_command", "command": ""}}}
$data modify storage mgs:temp dialog.body[0].contents[1].text set from storage mgs:maps $(mode)[$(idx)].name
$data modify storage mgs:temp dialog.yes.action.command set value "/function mgs:v5.3.0/maps/editor/delete {idx:$(idx),mode:$(mode)}"
$data modify storage mgs:temp dialog.no.action.command set value "/function mgs:v5.3.0/maps/editor/list/$(mode)"
function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

