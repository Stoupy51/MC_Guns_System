
#> mgs:v5.4.0/maps/multiplayer/hijacked/calls/start
#
# @within	#mgs:maps/start_script
#			mgs:v5.4.0/dialog/close_then
#

execute if data storage mgs:temp _base{mode:"multiplayer"} if data storage mgs:multiplayer game{state:"active"} if data storage mgs:multiplayer game{map_id:"hijacked"} run return run function mgs:v5.4.0/maps/multiplayer/hijacked/start

