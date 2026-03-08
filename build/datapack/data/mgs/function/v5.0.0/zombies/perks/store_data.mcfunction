
#> mgs:v5.0.0/zombies/perks/store_data
#
# @within	mgs:v5.0.0/zombies/perks/setup_iter with storage mgs:temp _pk_store
#
# @args		id (unknown)
#			perk_id (unknown)
#

$data modify storage mgs:zombies perk_data."$(id)" set value {perk_id:"$(perk_id)"}

