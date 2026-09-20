
#> mgs:v5.1.0/zombies/whos_who/load_snapshot
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/revive_complete with storage mgs:temp _ww_id
#
# @args		id (unknown)
#

$data modify storage mgs:temp _restore.items set from storage mgs:zombies ww_inv."$(id)"
$data remove storage mgs:zombies ww_inv."$(id)"

