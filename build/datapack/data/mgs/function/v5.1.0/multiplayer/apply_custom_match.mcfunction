
#> mgs:v5.1.0/multiplayer/apply_custom_match
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/apply_custom_found
#

# Copy found loadout's slots + perks to the format expected by apply_class_dynamic.
# apply_class_dynamic applies the slots and then calls apply_perks, which reads
# current_class.perks — so both standard classes and custom loadouts share one path.
data modify storage mgs:temp current_class set value {slots:[],perks:[]}
data modify storage mgs:temp current_class.slots set from storage mgs:temp _find_iter[0].slots
data modify storage mgs:temp current_class.perks set from storage mgs:temp _find_iter[0].perks
# Knife camo is cosmetic and lives outside slots[] (hotbar.0 is given unconditionally).
# Loadouts saved before knife camos existed have no field, so apply_class_dynamic defaults it.
execute if data storage mgs:temp _find_iter[0].knife_camo run data modify storage mgs:temp current_class.knife_camo set from storage mgs:temp _find_iter[0].knife_camo

# Apply the loadout (clears inventory, gives items, applies perks)
function mgs:v5.1.0/multiplayer/apply_class_dynamic

