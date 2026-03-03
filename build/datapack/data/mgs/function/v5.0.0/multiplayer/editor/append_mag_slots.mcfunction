
#> mgs:v5.0.0/multiplayer/editor/append_mag_slots
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save
#			mgs:v5.0.0/multiplayer/editor/start_secondary_mags
#

# Flatten mag_id for macro use (macro vars can't use dot-paths)
data modify storage mgs:temp _mag_id set from storage mgs:temp _mag_data.mag_id
data modify storage mgs:temp _mag_bullets set from storage mgs:temp _mag_data.mag_bullets

# Consumable mag: one slot only (with count and bullets)
execute if data storage mgs:temp _mag_data{mag_consumable:1b} run function mgs:v5.0.0/multiplayer/editor/append_mag_consumable
execute if data storage mgs:temp _mag_data{mag_consumable:1b} run return 0

# Non-consumable: add one slot per count
execute if score #pmag_count mgs.data matches 1.. run function mgs:v5.0.0/multiplayer/editor/append_mag_loop

