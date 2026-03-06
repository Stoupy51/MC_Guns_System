
#> mgs:v5.0.0/multiplayer/apply_class_dynamic
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/apply_class
#			mgs:v5.0.0/multiplayer/apply_custom_match
#

# Clear player inventory
clear @s

# Copy class slots to iteration temp
data modify storage mgs:temp slots set from storage mgs:temp current_class.slots

# Recursively apply all slots
execute if data storage mgs:temp slots[0] run function mgs:v5.0.0/multiplayer/apply_next_slot

