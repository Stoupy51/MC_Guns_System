
#> mgs:v5.4.1/multiplayer/editor/load_state
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/config/process with storage mgs:temp
#
# @args		_pid (unknown)
#

# The player's slot is created first: on a failed copy (first use), mgs:temp editor would keep another player's state.
$execute unless data storage mgs:editor "$(_pid)" run data modify storage mgs:editor "$(_pid)" set value {}
$data modify storage mgs:temp editor set from storage mgs:editor "$(_pid)"

