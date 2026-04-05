
#> mgs:v5.0.0/multiplayer/editor/save_state
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process with storage mgs:temp
#
# @args		_pid (unknown)
#

$data modify storage mgs:editor "$(_pid)" set from storage mgs:temp editor

