
#> mgs:v5.0.0/zombies/doors/remove_block_destroy
#
# @executed	as @e[tag=mgs.door] & at @s
#
# @within	mgs:v5.0.0/zombies/doors/open_one with storage mgs:temp _door_open
#
# @args		rot (unknown)
#			offset (unknown)
#

$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run setblock ~ ~ ~ air destroy
$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run kill @e[type=item,distance=..1.5]

