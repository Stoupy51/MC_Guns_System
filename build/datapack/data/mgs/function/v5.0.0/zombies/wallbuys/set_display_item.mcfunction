
#> mgs:v5.0.0/zombies/wallbuys/set_display_item
#
# @within	mgs:v5.0.0/zombies/wallbuys/setup_iter with storage mgs:temp _wb
#
# @args		weapon_id (unknown)
#

$execute as @e[tag=mgs.wb_new_display] run loot replace entity @s contents loot mgs:i/$(weapon_id)

