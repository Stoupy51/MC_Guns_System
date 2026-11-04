
#> mgs:v5.3.0/maps/zombies/kino_der_toten/calls/respawn
#
# @within	#mgs:maps/respawn_script
#			mgs:v5.3.0/dialog/close_then
#

execute if data storage mgs:temp _base{mode:"zombies"} if data storage mgs:zombies game{state:"active"} if data storage mgs:zombies game{map_id:"kino_der_toten"} run return run function mgs:v5.3.0/maps/zombies/kino_der_toten/respawn

