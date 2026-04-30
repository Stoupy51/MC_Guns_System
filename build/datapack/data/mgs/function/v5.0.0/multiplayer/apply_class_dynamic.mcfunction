
#> mgs:v5.0.0/multiplayer/apply_class_dynamic
#
# @within	mgs:v5.0.0/multiplayer/apply_class
#			mgs:v5.0.0/multiplayer/apply_custom_match
#

# Clear player inventory
clear @s

# Apply armor
item replace entity @s armor.head with air
item replace entity @s armor.chest with leather_chestplate[dyed_color=10263702,unbreakable={}]
item replace entity @s armor.legs with chainmail_leggings[unbreakable={}]
item replace entity @s armor.feet with iron_boots[unbreakable={}]

# Copy class slots to iteration temp
data modify storage mgs:temp slots set from storage mgs:temp current_class.slots

# Recursively apply all slots
execute if data storage mgs:temp slots[0] run function mgs:v5.0.0/multiplayer/apply_next_slot

# Give class menu item (only in multiplayer)
execute if entity @s[tag=mgs.give_class_menu] run loot replace entity @s hotbar.4 loot mgs:i/class_menu

