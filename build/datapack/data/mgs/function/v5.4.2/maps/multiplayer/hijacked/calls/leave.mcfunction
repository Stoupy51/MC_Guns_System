
#> mgs:v5.4.2/maps/multiplayer/hijacked/calls/leave
#
# @within	#mgs:maps/leave_script
#			mgs:v5.4.2/dialog/close_then
#

execute if data storage mgs:temp _base{mode:"multiplayer"} unless data storage mgs:multiplayer game{state:"lobby"} if data storage mgs:multiplayer game{map_id:"hijacked"} run return run function mgs:v5.4.2/maps/multiplayer/hijacked/leave

