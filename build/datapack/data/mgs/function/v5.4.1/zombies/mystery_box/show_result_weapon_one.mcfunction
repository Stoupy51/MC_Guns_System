
#> mgs:v5.4.1/zombies/mystery_box/show_result_weapon_one
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/mystery_box/show_result_one with storage mgs:zombies mystery_box.result
#
# @args		weapon_id (unknown)
#

$loot replace entity @s contents loot mgs:i/$(weapon_id)

