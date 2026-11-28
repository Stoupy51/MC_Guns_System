
#> mgs:v5.4.4/multiplayer/apply_class_dynamic
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/multiplayer/apply_class
#			mgs:v5.4.4/multiplayer/apply_custom_match
#

clear @s

item replace entity @s armor.head with air
item replace entity @s armor.chest with leather_chestplate[dyed_color=10263702,unbreakable={},attribute_modifiers=[{type:"minecraft:armor",id:"mgs:armor_chest",amount:5,operation:"add_value",slot:"chest"}]]
item replace entity @s armor.legs with chainmail_leggings[unbreakable={},attribute_modifiers=[{type:"minecraft:armor",id:"mgs:armor_legs",amount:5,operation:"add_value",slot:"legs"}]]
item replace entity @s armor.feet with iron_boots[unbreakable={},attribute_modifiers=[{type:"minecraft:armor",id:"mgs:armor_feet",amount:5,operation:"add_value",slot:"feet"}]]

# The knife is always given in hotbar.0, so weapons start at hotbar.1 and hotbar.2. The camo defaults to "":
# standard classes never set it, and older loadouts have no field, which would fail the macro.
data modify storage mgs:temp _knife set value {camo:""}
execute if data storage mgs:temp current_class.knife_camo run data modify storage mgs:temp _knife.camo set from storage mgs:temp current_class.knife_camo
function mgs:v5.4.4/multiplayer/apply_knife with storage mgs:temp _knife

data modify storage mgs:temp slots set from storage mgs:temp current_class.slots

execute if data storage mgs:temp slots[0] run function mgs:v5.4.4/multiplayer/apply_next_slot

function mgs:v5.4.4/multiplayer/apply_perks

# Multiplayer only.
execute if entity @s[tag=mgs.give_class_menu] run loot replace entity @s hotbar.4 loot mgs:i/class_menu

