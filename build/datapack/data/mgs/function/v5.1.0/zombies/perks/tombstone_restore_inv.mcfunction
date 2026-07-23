
#> mgs:v5.1.0/zombies/perks/tombstone_restore_inv
#
# @executed	as @a[distance=..2,gamemode=!spectator,scores={mgs.zb.in_game=1,mgs.zb.downed=0}]
#
# @within	mgs:v5.1.0/zombies/perks/tombstone_collect with storage mgs:temp _ts_id
#
# @args		id (unknown)
#

$data modify entity @s Inventory set from storage mgs:zombies tombstone_inv."$(id)"
$data remove storage mgs:zombies tombstone_inv."$(id)"

