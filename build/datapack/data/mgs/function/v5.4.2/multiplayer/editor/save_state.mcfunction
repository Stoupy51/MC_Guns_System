
#> mgs:v5.4.2/multiplayer/editor/save_state
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/config/process with storage mgs:temp
#
# @args		_pid (unknown)
#

$data modify storage mgs:editor "$(_pid)" set from storage mgs:temp editor

