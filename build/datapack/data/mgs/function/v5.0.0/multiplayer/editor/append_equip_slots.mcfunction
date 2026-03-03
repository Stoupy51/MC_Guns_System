
#> mgs:v5.0.0/multiplayer/editor/append_equip_slots
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save
#			mgs:v5.0.0/multiplayer/editor/append_equip_slots
#

# Append the first equipment slot
data modify storage mgs:temp _new_loadout.slots append from storage mgs:temp _build.equipment_data.slots[0]

# Remove and recurse
data remove storage mgs:temp _build.equipment_data.slots[0]
execute if data storage mgs:temp _build.equipment_data.slots[0] run function mgs:v5.0.0/multiplayer/editor/append_equip_slots

