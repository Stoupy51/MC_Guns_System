
#> mgs:v5.4.2/zombies/perks/tombstone_clear_inv
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/perks/tombstone_expire with storage mgs:temp _ts_id
#
# @args		id (unknown)
#

$data remove storage mgs:zombies tombstone_inv."$(id)"

