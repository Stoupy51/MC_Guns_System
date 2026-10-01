
#> mgs:v5.1.0/multiplayer/apply_class_dynamic
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/apply_class
#			mgs:v5.1.0/multiplayer/apply_custom_match
#

clear @s

item replace entity @s armor.head with air
item replace entity @s armor.chest with leather_chestplate[dyed_color=10263702,unbreakable={}]
item replace entity @s armor.legs with chainmail_leggings[unbreakable={}]
item replace entity @s armor.feet with iron_boots[unbreakable={}]

# The knife is always given in hotbar.0, so weapons start at hotbar.1 and hotbar.2. The camo defaults to "":
# standard classes never set it, and older loadouts have no field, which would fail the macro.
data modify storage mgs:temp _knife set value {camo:""}
execute if data storage mgs:temp current_class.knife_camo run data modify storage mgs:temp _knife.camo set from storage mgs:temp current_class.knife_camo
function mgs:v5.1.0/multiplayer/apply_knife with storage mgs:temp _knife

data modify storage mgs:temp slots set from storage mgs:temp current_class.slots

execute if data storage mgs:temp slots[0] run function mgs:v5.1.0/multiplayer/apply_next_slot

function mgs:v5.1.0/multiplayer/apply_perks

# Multiplayer only.
execute if entity @s[tag=mgs.give_class_menu] run loot replace entity @s hotbar.4 loot mgs:i/class_menu

