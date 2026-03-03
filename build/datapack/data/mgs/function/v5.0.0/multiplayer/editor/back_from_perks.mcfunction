
#> mgs:v5.0.0/multiplayer/editor/back_from_perks
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Refund equip_slot2 grenade cost if one was selected
execute unless data storage mgs:temp editor{equip_slot2:""} run scoreboard players add @s mgs.mp.edit_points 1
# Clear equip_slot2 state and perks list
data modify storage mgs:temp editor.equip_slot2 set value ""
data modify storage mgs:temp editor.perks set value []
# Show equip slot 2 dialog
function mgs:v5.0.0/multiplayer/editor/show_equip_slot2_dialog

