
#> mgs:v5.0.0/multiplayer/editor/load_state
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process with storage mgs:temp
#
# @args		_pid (unknown)
#

$data modify storage mgs:temp editor set from storage mgs:editor "$(_pid)"

