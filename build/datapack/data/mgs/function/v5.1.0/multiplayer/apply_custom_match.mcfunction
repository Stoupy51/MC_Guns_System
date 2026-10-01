
#> mgs:v5.1.0/multiplayer/apply_custom_match
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/apply_custom_found
#

# Same layout as a standard class, so both go through apply_class_dynamic, which then applies current_class.perks.
data modify storage mgs:temp current_class set value {slots:[],perks:[]}
data modify storage mgs:temp current_class.slots set from storage mgs:temp _find_iter[0].slots
data modify storage mgs:temp current_class.perks set from storage mgs:temp _find_iter[0].perks
# The knife camo lives outside slots[] (hotbar.0 is always given); loadouts saved before knife camos have none, and apply_class_dynamic defaults it.
execute if data storage mgs:temp _find_iter[0].knife_camo run data modify storage mgs:temp current_class.knife_camo set from storage mgs:temp _find_iter[0].knife_camo

function mgs:v5.1.0/multiplayer/apply_class_dynamic

