
#> mgs:v5.0.0/zombies/perks/lookup_perk
#
# @within	mgs:v5.0.0/zombies/perks/on_right_click with storage mgs:temp _pk_buy
#
# @args		id (unknown)
#

$data modify storage mgs:temp _pk_data set from storage mgs:zombies perk_data."$(id)"

