
#> mgs:v5.4.0/zombies/whos_who/discard_snapshot
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/whos_who/forfeit with storage mgs:temp _ww_id
#
# @args		id (unknown)
#

$data remove storage mgs:zombies ww_inv."$(id)"

