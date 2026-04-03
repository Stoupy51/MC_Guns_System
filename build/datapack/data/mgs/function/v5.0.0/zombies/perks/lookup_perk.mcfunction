
#> mgs:v5.0.0/zombies/perks/lookup_perk
#
# @executed	as @n[tag=mgs.pk_new]
#
# @within	mgs:v5.0.0/zombies/perks/on_right_click with storage mgs:temp _pk_buy
#			mgs:v5.0.0/zombies/perks/on_hover with storage mgs:temp _pk_hover
#
# @args		id (unknown)
#

$data modify storage mgs:temp _pk_data set from storage mgs:zombies perk_data."$(id)"

