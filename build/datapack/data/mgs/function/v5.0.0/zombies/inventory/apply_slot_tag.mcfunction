
#> mgs:v5.0.0/zombies/inventory/apply_slot_tag
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/inventory/give_starting_loadout {slot:"hotbar.0",group:"hotbar",index:0}
#			mgs:v5.0.0/zombies/inventory/give_starting_loadout {slot:"hotbar.1",group:"hotbar",index:1}
#			mgs:v5.0.0/zombies/inventory/give_starting_loadout {slot:"inventory.1",group:"inventory",index:1}
#			mgs:v5.0.0/zombies/inventory/give_starting_loadout {slot:"hotbar.7",group:"hotbar",index:7}
#			mgs:v5.0.0/zombies/inventory/refresh_info_item {slot:"hotbar.8",group:"hotbar",index:8}
#			mgs:v5.0.0/zombies/inventory/give_ability_item {slot:"hotbar.4",group:"hotbar",index:4}
#			mgs:v5.0.0/zombies/inventory/recreate_critical_items {slot:"hotbar.0",group:"hotbar",index:0}
#			mgs:v5.0.0/zombies/inventory/recreate_critical_items {slot:"hotbar.7",group:"hotbar",index:7}
#			mgs:v5.0.0/zombies/mystery_box/give_consumable_slot {slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}
#			mgs:v5.0.0/zombies/wallbuys/give_to_slot {slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}
#			mgs:v5.0.0/zombies/wallbuys/give_to_slot {slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}
#			mgs:v5.0.0/zombies/wallbuys/reload_pair {slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}
#			mgs:v5.0.0/zombies/wallbuys/reload_pair {slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}
#			mgs:v5.0.0/zombies/wallbuys/replace_pair {slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}
#			mgs:v5.0.0/zombies/wallbuys/replace_pair {slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}
#
# @args		group (string)
#			index (int)
#			slot (string)
#

data modify storage mgs:temp zb_slot set value {}
$data modify storage mgs:temp zb_slot.$(group) set value $(index)
$item modify entity @s $(slot) mgs:v5.0.0/zb_slot_tag

