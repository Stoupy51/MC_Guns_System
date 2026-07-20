
#> mgs:v5.1.0/zombies/inventory/give_lethal_type
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/bonus/max_ammo_grenades {count:4}
#			mgs:v5.1.0/zombies/inventory/replenish_grenades {count:2}
#
# @args		count (int)
#

function mgs:v5.1.0/zombies/inventory/loot_replace_lethal
$item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_$(count)
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}

