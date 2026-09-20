
#> mgs:v5.1.0/zombies/perks/tombstone_snapshot_inv
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/perks/tombstone_on_bleed_out with storage mgs:temp _ts_id
#
# @args		id (unknown)
#

$data modify storage mgs:zombies tombstone_inv."$(id)" set from entity @s Inventory

