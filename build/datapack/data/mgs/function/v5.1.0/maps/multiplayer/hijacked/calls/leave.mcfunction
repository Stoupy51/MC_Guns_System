
#> mgs:v5.1.0/maps/multiplayer/hijacked/calls/leave
#
# @within	#mgs:maps/leave_script
#

execute if data storage mgs:multiplayer game{state:"active"} if data storage mgs:multiplayer game{map_id:"hijacked"} run return run function mgs:v5.1.0/maps/multiplayer/hijacked/leave

