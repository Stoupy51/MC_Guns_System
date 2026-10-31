
#> mgs:v5.3.0/zombies/mystery_box/close_lid
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.3.0/zombies/mystery_box/show_bear_result
#			mgs:v5.3.0/zombies/mystery_box/collect
#			mgs:v5.3.0/zombies/mystery_box/reset_one
#

execute as @n[tag=mgs.mb_lid,distance=..4] run function mgs:v5.3.0/zombies/mystery_box/lid_close

