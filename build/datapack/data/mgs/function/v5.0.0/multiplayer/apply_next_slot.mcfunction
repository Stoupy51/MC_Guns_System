
#> mgs:v5.0.0/multiplayer/apply_next_slot
#
# @within	mgs:v5.0.0/multiplayer/apply_next_slot
#			mgs:v5.0.0/multiplayer/apply_class_dynamic
#

# Apply loot to slot
data modify storage mgs:temp current_slot set from storage mgs:temp slots[0]
function mgs:v5.0.0/multiplayer/apply_slot_loot with storage mgs:temp current_slot

# If count > 1, apply set_count modifier
execute unless data storage mgs:temp current_slot{count:1} run function mgs:v5.0.0/multiplayer/apply_slot_count with storage mgs:temp current_slot

# If consumable, apply consumable count modifier
execute if data storage mgs:temp current_slot{consumable:true} run function mgs:v5.0.0/multiplayer/apply_slot_consumable with storage mgs:temp current_slot

# Remove processed slot and recurse
data remove storage mgs:temp slots[0]
execute if data storage mgs:temp slots[0] run function mgs:v5.0.0/multiplayer/apply_next_slot

