
#> mgs:v5.0.1/maps/multiplayer/hijacked/calls/respawn
#
# @within	#mgs:maps/respawn_script
#

execute if data storage mgs:multiplayer game{state:"active"} if data storage mgs:multiplayer game{map_id:"hijacked"} run return run function mgs:v5.0.1/maps/multiplayer/hijacked/respawn

