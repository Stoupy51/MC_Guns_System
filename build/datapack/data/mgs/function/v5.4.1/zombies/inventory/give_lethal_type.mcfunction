
#> mgs:v5.4.1/zombies/inventory/give_lethal_type
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/bonus/max_ammo_grenades {count:4}
#			mgs:v5.4.1/zombies/inventory/replenish_grenades {count:2}
#
# @args		count (int)
#

function mgs:v5.4.1/zombies/inventory/loot_replace_lethal
$item modify entity @s hotbar.7 mgs:v5.4.1/grenade/set_count_$(count)
function mgs:v5.4.1/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}

