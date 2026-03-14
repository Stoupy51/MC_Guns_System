
#> mgs:v5.0.0/zombies/mystery_box/show_result_weapon
#
# @within	mgs:v5.0.0/zombies/mystery_box/show_result with storage mgs:zombies mystery_box.result
#
# @args		weapon_id (unknown)
#

$loot replace entity @n[tag=mgs.mb_display] contents loot mgs:i/$(weapon_id)

