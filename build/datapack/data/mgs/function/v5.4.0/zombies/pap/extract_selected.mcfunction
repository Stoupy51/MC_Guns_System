
#> mgs:v5.4.0/zombies/pap/extract_selected
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/pap/on_right_click with storage mgs:temp _pap
#			mgs:v5.4.0/zombies/pap/upgrade_core with storage mgs:temp _pap
#
# @args		slot (unknown)
#

tag @s add mgs.pap_extracting
$execute summon item_display run function mgs:v5.4.0/zombies/pap/extract_selected_item {slot:"$(slot)"}
tag @s remove mgs.pap_extracting

