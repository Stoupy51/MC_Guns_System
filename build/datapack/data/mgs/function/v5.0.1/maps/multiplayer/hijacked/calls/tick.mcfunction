
#> mgs:v5.0.1/maps/multiplayer/hijacked/calls/tick
#
# @within	#mgs:maps/tick_script
#

execute if data storage mgs:multiplayer game{state:"active"} if data storage mgs:multiplayer game{map_id:"hijacked"} run return run function mgs:v5.0.1/maps/multiplayer/hijacked/tick

