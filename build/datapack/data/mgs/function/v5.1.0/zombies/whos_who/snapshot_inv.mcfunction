
#> mgs:v5.1.0/zombies/whos_who/snapshot_inv
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/on_down with storage mgs:temp _ww_id
#
# @args		id (unknown)
#

$data modify storage mgs:zombies ww_inv."$(id)" set from entity @s Inventory

