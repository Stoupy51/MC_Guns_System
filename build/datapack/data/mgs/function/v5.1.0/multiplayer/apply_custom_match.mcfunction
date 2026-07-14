
#> mgs:v5.1.0/multiplayer/apply_custom_match
#
# @within	mgs:v5.1.0/multiplayer/apply_custom_found
#

# Copy found loadout's slots + perks to the format expected by apply_class_dynamic.
# apply_class_dynamic applies the slots and then calls apply_perks, which reads
# current_class.perks — so both standard classes and custom loadouts share one path.
data modify storage mgs:temp current_class set value {slots:[],perks:[]}
data modify storage mgs:temp current_class.slots set from storage mgs:temp _find_iter[0].slots
data modify storage mgs:temp current_class.perks set from storage mgs:temp _find_iter[0].perks

# Apply the loadout (clears inventory, gives items, applies perks)
function mgs:v5.1.0/multiplayer/apply_class_dynamic

