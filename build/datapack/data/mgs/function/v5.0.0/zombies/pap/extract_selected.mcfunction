
#> mgs:v5.0.0/zombies/pap/extract_selected
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click with storage mgs:temp _pap
#			mgs:v5.0.0/zombies/pap/on_free_pap with storage mgs:temp _pap
#
# @args		slot (unknown)
#

tag @s add mgs.pap_extracting
$execute summon item_display run function mgs:v5.0.0/zombies/pap/extract_selected_item {slot:"$(slot)"}
tag @s remove mgs.pap_extracting

