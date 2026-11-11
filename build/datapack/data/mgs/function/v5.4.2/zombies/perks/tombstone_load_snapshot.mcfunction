
#> mgs:v5.4.2/zombies/perks/tombstone_load_snapshot
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/perks/tombstone_collect with storage mgs:temp _ts_id
#
# @args		id (unknown)
#

$data modify storage mgs:temp _restore.items set from storage mgs:zombies tombstone_inv."$(id)"
$data remove storage mgs:zombies tombstone_inv."$(id)"

