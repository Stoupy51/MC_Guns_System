
#> mgs:v5.1.0/multiplayer/editor/load_state
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process with storage mgs:temp
#
# @args		_pid (unknown)
#

# The player's slot is created first: on a failed copy (first use), mgs:temp editor would keep another player's state.
$execute unless data storage mgs:editor "$(_pid)" run data modify storage mgs:editor "$(_pid)" set value {}
$data modify storage mgs:temp editor set from storage mgs:editor "$(_pid)"

