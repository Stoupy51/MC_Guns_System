
#> mgs:v5.0.0/multiplayer/editor/show_confirm
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_equipment with storage mgs:temp editor
#
# @args		primary_name (unknown)
#			primary_scope_name (unknown)
#			secondary_name (unknown)
#			secondary_scope_name (unknown)
#			equipment_name (unknown)
#

# Build summary body using macro substitution
$data modify storage mgs:temp dialog.body set value [{type:"minecraft:plain_message",contents:["",{"translate": "mgs.primary","color":"white"},{"text":"$(primary_name)","color":"green","bold":true},{"text":" ($(primary_scope_name))","color":"dark_green"}]},{type:"minecraft:plain_message",contents:["",{"translate": "mgs.secondary","color":"white"},{"text":"$(secondary_name)","color":"yellow","bold":true},{"text":" ($(secondary_scope_name))","color":"gold"}]},{type:"minecraft:plain_message",contents:["",{"translate": "mgs.equipment","color":"white"},{"text":"$(equipment_name)","color":"aqua","bold":true}]},{type:"minecraft:plain_message",contents:{translate: "mgs.save_this_loadout","color":"gray"}}]

# Show the dialog
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

