
#> mgs:v5.0.0/zombies/mystery_box/capture_collected_name_slot
#
# @within	mgs:v5.0.0/zombies/mystery_box/capture_collected_name {slot:"hotbar.1"}
#			mgs:v5.0.0/zombies/mystery_box/capture_collected_name {slot:"hotbar.2"}
#			mgs:v5.0.0/zombies/mystery_box/capture_collected_name {slot:"hotbar.3"}
#
# @args		slot (string)
#

tag @s add mgs.mb_name_reader
$execute summon item_display run function mgs:v5.0.0/zombies/mystery_box/extract_collected_item_name {slot:"$(slot)"}
tag @s remove mgs.mb_name_reader
scoreboard players set #mb_name_found mgs.data 1

