
#> mgs:v5.0.1/multiplayer/editor/back_to_equip1
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

# Refund grenade costs for both slots (slot 2 is set when backing out of its camo dialog)
execute unless data storage mgs:temp editor{equip_slot1:""} run scoreboard players add @s mgs.mp.edit_points 1
execute unless data storage mgs:temp editor{equip_slot2:""} run scoreboard players add @s mgs.mp.edit_points 1
# Clear equipment state
data modify storage mgs:temp editor.equip_slot1 set value ""
data modify storage mgs:temp editor.equip_slot1_camo set value ""
data modify storage mgs:temp editor.equip_slot2 set value ""
data modify storage mgs:temp editor.equip_slot2_camo set value ""
# Show equip slot 1 dialog
function mgs:v5.0.1/multiplayer/editor/show_equip_slot1_dialog

