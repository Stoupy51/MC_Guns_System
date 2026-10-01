
#> mgs:v5.1.0/multiplayer/apply_next_slot
#
# @within	mgs:v5.1.0/multiplayer/apply_next_slot
#			mgs:v5.1.0/multiplayer/apply_class_dynamic
#

data modify storage mgs:temp current_slot set from storage mgs:temp slots[0]
function mgs:v5.1.0/multiplayer/apply_slot_loot with storage mgs:temp current_slot

execute unless data storage mgs:temp current_slot{count:1} run function mgs:v5.1.0/multiplayer/apply_slot_count with storage mgs:temp current_slot

execute if data storage mgs:temp current_slot{consumable:true} run function mgs:v5.1.0/multiplayer/apply_slot_consumable with storage mgs:temp current_slot

data remove storage mgs:temp slots[0]
execute if data storage mgs:temp slots[0] run function mgs:v5.1.0/multiplayer/apply_next_slot

