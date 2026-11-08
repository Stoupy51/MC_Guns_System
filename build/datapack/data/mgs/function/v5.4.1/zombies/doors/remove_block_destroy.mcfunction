
#> mgs:v5.4.1/zombies/doors/remove_block_destroy
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/doors/open_one with storage mgs:temp _door_open
#
# @args		rot (unknown)
#			offset (unknown)
#

$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run setblock ~ ~ ~ air destroy
$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run kill @e[type=item,distance=..1.5]

