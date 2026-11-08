
#> mgs:v5.4.1/maps/zombies/kino_der_toten/calls/start
#
# @within	#mgs:maps/start_script
#			mgs:v5.4.1/dialog/close_then
#

execute if data storage mgs:temp _base{mode:"zombies"} if data storage mgs:zombies game{state:"active"} if data storage mgs:zombies game{map_id:"kino_der_toten"} run return run function mgs:v5.4.1/maps/zombies/kino_der_toten/start

