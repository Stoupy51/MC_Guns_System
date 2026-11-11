
#> mgs:v5.4.2/zombies/doors/remove_block_silent
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/doors/open_one with storage mgs:temp _door_open
#
# @args		rot (unknown)
#			offset (unknown)
#

$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run setblock ~ ~ ~ air

