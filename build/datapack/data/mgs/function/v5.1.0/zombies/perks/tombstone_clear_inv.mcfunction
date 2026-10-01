
#> mgs:v5.1.0/zombies/perks/tombstone_clear_inv
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/perks/tombstone_expire with storage mgs:temp _ts_id
#
# @args		id (unknown)
#

$data remove storage mgs:zombies tombstone_inv."$(id)"

