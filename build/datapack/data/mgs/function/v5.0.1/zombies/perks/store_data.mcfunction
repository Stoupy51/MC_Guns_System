
#> mgs:v5.0.1/zombies/perks/store_data
#
# @within	mgs:v5.0.1/zombies/perks/setup_iter with storage mgs:temp _pk_store
#
# @args		id (unknown)
#			perk_id (unknown)
#			name (unknown)
#

$data modify storage mgs:zombies perk_data."$(id)" set value {perk_id:"$(perk_id)",name:"$(name)"}

