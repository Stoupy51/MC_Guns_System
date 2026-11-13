
#> mgs:v5.4.2/zombies/save/forget_door_link
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/capture_door_open with storage mgs:temp _sv_link
#
# @args		id (unknown)
#

$data remove storage mgs:temp _sv_doors[{link_id:$(id)}]

