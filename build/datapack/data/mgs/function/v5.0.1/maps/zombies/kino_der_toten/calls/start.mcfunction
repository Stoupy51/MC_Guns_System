
#> mgs:v5.0.1/maps/zombies/kino_der_toten/calls/start
#
# @within	#mgs:maps/start_script
#

execute if data storage mgs:zombies game{state:"active"} if data storage mgs:zombies game{map_id:"kino_der_toten"} run return run function mgs:v5.0.1/maps/zombies/kino_der_toten/start

