
#> mgs:v5.1.0/zombies/mystery_box/cycle_display_weapon_one
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/cycle_display_one with storage mgs:temp _mb_cycle_item
#
# @args		weapon_id (unknown)
#

$loot replace entity @s contents loot mgs:i/$(weapon_id)

