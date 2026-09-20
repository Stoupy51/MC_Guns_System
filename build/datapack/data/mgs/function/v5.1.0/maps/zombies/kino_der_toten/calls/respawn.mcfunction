
#> mgs:v5.1.0/maps/zombies/kino_der_toten/calls/respawn
#
# @within	#mgs:maps/respawn_script
#

execute if data storage mgs:zombies game{state:"active"} if data storage mgs:zombies game{map_id:"kino_der_toten"} run return run function mgs:v5.1.0/maps/zombies/kino_der_toten/respawn

