
#> mgs:v5.1.0/zombies/wallbuys/give_tactical
#
# @within	mgs:v5.1.0/zombies/mystery_box/default_give/monkey_bomb {weapon_id:"monkey_bomb"}
#
# @args		weapon_id (string)
#

scoreboard players set #wb_purchase_done mgs.data 1
scoreboard players set #wb_purchase_mode mgs.data 2

# Already carrying the same tactical: top it back up to 3
$execute if items entity @s hotbar.6 *[custom_data~{mgs:{$(weapon_id):true}}] run return run item modify entity @s hotbar.6 mgs:v5.1.0/grenade/set_count_3

# Fresh give: 3 in the tactical slot (hotbar.6), tagged for the zombies slot enforcement
$loot replace entity @s hotbar.6 loot mgs:i/$(weapon_id)
item modify entity @s hotbar.6 mgs:v5.1.0/grenade/set_count_3
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.6",group:"hotbar",index:6}
scoreboard players set #wb_purchase_mode mgs.data 1

