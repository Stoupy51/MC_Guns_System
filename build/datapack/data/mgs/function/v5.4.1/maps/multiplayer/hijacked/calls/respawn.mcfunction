
#> mgs:v5.4.1/maps/multiplayer/hijacked/calls/respawn
#
# @within	#mgs:maps/respawn_script
#			mgs:v5.4.1/dialog/close_then
#

execute if data storage mgs:temp _base{mode:"multiplayer"} unless data storage mgs:multiplayer game{state:"lobby"} if data storage mgs:multiplayer game{map_id:"hijacked"} run return run function mgs:v5.4.1/maps/multiplayer/hijacked/respawn

