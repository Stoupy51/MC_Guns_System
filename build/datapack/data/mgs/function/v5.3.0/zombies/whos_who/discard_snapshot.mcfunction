
#> mgs:v5.3.0/zombies/whos_who/discard_snapshot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/zombies/whos_who/forfeit with storage mgs:temp _ww_id
#
# @args		id (unknown)
#

$data remove storage mgs:zombies ww_inv."$(id)"

