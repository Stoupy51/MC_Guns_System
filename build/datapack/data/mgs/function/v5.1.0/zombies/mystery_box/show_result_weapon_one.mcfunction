
#> mgs:v5.1.0/zombies/mystery_box/show_result_weapon_one
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/show_result_one with storage mgs:zombies mystery_box.result
#
# @args		weapon_id (unknown)
#

$loot replace entity @s contents loot mgs:i/$(weapon_id)

