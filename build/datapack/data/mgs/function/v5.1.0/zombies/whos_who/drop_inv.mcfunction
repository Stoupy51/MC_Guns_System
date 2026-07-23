
#> mgs:v5.1.0/zombies/whos_who/drop_inv
#
# @executed	as @a[tag=mgs.ww_active,scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/whos_who/bleed_out with storage mgs:temp _ww_id
#
# @args		id (unknown)
#

$data remove storage mgs:zombies ww_inv."$(id)"

