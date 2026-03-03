
#> mgs:v5.0.0/multiplayer/custom/apply_found
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/find_and_apply
#

# Copy found loadout's slots to the format expected by apply_class_dynamic
data modify storage mgs:temp current_class set value {slots:[]}
data modify storage mgs:temp current_class.slots set from storage mgs:temp _find_iter[0].slots

# Apply the loadout (clears inventory and gives items)
function mgs:v5.0.0/multiplayer/apply_class_dynamic

# Notify player
function mgs:v5.0.0/multiplayer/custom/notify_selected with storage mgs:temp _find_iter[0]

