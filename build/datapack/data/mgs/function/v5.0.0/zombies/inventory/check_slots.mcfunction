
#> mgs:v5.0.0/zombies/inventory/check_slots
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/on_change
#

# hard forbidden slot
execute if items entity @s hotbar.5 * run function mgs:v5.0.0/zombies/inventory/drop_wrong_slot_item {slot:"hotbar.5"}

# Always-enforced slots
function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"hotbar.8",match:"*[custom_data~{mgs:{zb_info:true,zombies:{hotbar:8}}}]",expected_nbt:{mgs:{zb_info:true,zombies:{hotbar:8}}}}
function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"hotbar.7",match:"*[custom_data~{mgs:{gun:true,zombies:{hotbar:7}}}]",expected_nbt:{mgs:{gun:true,zombies:{hotbar:7}}}}
function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"hotbar.6",match:"*[custom_data~{mgs:{gun:true,zombies:{hotbar:6}}}]",expected_nbt:{mgs:{gun:true,zombies:{hotbar:6}}}}
function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"hotbar.2",match:"*[custom_data~{mgs:{gun:true,zombies:{hotbar:2}}}]",expected_nbt:{mgs:{gun:true,zombies:{hotbar:2}}}}
function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"hotbar.1",match:"*[custom_data~{mgs:{gun:true,zombies:{hotbar:1}}}]",expected_nbt:{mgs:{gun:true,zombies:{hotbar:1}}}}
function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"hotbar.0",match:"*[custom_data~{mgs:{knife:true,zombies:{hotbar:0}}}]",expected_nbt:{mgs:{knife:true,zombies:{hotbar:0}}}}
function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"inventory.1",match:"*[custom_data~{mgs:{magazine:true,zombies:{inventory:1}}}]",expected_nbt:{mgs:{magazine:true,zombies:{inventory:1}}}}
function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"inventory.2",match:"*[custom_data~{mgs:{magazine:true,zombies:{inventory:2}}}]",expected_nbt:{mgs:{magazine:true,zombies:{inventory:2}}}}

# Mule kick gates the third weapon/magazine slots only.
execute if score @s mgs.zb.perk.mule_kick matches 1 run function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"hotbar.3",match:"*[custom_data~{mgs:{gun:true,zombies:{hotbar:3}}}]",expected_nbt:{mgs:{gun:true,zombies:{hotbar:3}}}}
execute if score @s mgs.zb.perk.mule_kick matches 1 run function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"inventory.3",match:"*[custom_data~{mgs:{magazine:true,zombies:{inventory:3}}}]",expected_nbt:{mgs:{magazine:true,zombies:{inventory:3}}}}
execute unless score @s mgs.zb.perk.mule_kick matches 1 run item replace entity @s hotbar.3 with air
execute unless score @s mgs.zb.perk.mule_kick matches 1 run item replace entity @s inventory.3 with air

# Ability slot is only for manual abilities (automatic abilities such as coward should not show item)
execute if score @s mgs.zb.ability matches 3.. run function mgs:v5.0.0/zombies/inventory/enforce_slot {slot:"hotbar.4",match:"*[custom_data~{mgs:{zb_ability_item:true,zombies:{hotbar:4}}}]",expected_nbt:{mgs:{zb_ability_item:true,zombies:{hotbar:4}}}}
execute unless score @s mgs.zb.ability matches 3.. run item replace entity @s hotbar.4 with air

# Clear cursor (prevent dragging tagged items outside managed inventory)
execute if items entity @s player.cursor * run function mgs:v5.0.0/zombies/inventory/drop_wrong_slot_item {slot:"player.cursor"}

