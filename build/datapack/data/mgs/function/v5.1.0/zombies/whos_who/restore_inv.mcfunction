
#> mgs:v5.1.0/zombies/whos_who/restore_inv
#
# @executed	as @a[tag=mgs.ww_active,scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/whos_who/revive_complete with storage mgs:temp _ww_id
#
# @args		id (unknown)
#

$data modify entity @s Inventory set from storage mgs:zombies ww_inv."$(id)"
$data remove storage mgs:zombies ww_inv."$(id)"

