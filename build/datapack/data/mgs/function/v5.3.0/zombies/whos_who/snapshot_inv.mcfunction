
#> mgs:v5.3.0/zombies/whos_who/snapshot_inv
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/whos_who/on_down with storage mgs:temp _ww_id
#
# @args		id (unknown)
#

$data modify storage mgs:zombies ww_inv."$(id)" set from entity @s Inventory

