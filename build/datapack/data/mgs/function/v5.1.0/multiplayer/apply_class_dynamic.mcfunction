
#> mgs:v5.1.0/multiplayer/apply_class_dynamic
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/apply_class
#			mgs:v5.1.0/multiplayer/apply_custom_match
#

# Clear player inventory
clear @s

# Apply armor
item replace entity @s armor.head with air
item replace entity @s armor.chest with leather_chestplate[dyed_color=10263702,unbreakable={}]
item replace entity @s armor.legs with chainmail_leggings[unbreakable={}]
item replace entity @s armor.feet with iron_boots[unbreakable={}]

# Knife in hotbar.0 for every loadout: it is not part of the class slot list because no class can
# choose it away. Weapons therefore start at hotbar.1 (primary) and hotbar.2 (secondary).
# Default the camo first: standard classes never set it, and loadouts saved before knife camos
# existed have no field, so the macro would fail on a missing $(camo).
data modify storage mgs:temp _knife set value {camo:""}
execute if data storage mgs:temp current_class.knife_camo run data modify storage mgs:temp _knife.camo set from storage mgs:temp current_class.knife_camo
function mgs:v5.1.0/multiplayer/apply_knife with storage mgs:temp _knife

# Copy class slots to iteration temp
data modify storage mgs:temp slots set from storage mgs:temp current_class.slots

# Recursively apply all slots
execute if data storage mgs:temp slots[0] run function mgs:v5.1.0/multiplayer/apply_next_slot

# Apply perks from the selected loadout (standard class or custom)
function mgs:v5.1.0/multiplayer/apply_perks

# Give class menu item (only in multiplayer)
execute if entity @s[tag=mgs.give_class_menu] run loot replace entity @s hotbar.4 loot mgs:i/class_menu

