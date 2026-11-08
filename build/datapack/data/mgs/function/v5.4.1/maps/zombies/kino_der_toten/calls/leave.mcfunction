
#> mgs:v5.4.1/maps/zombies/kino_der_toten/calls/leave
#
# @within	#mgs:maps/leave_script
#			mgs:v5.4.1/dialog/close_then
#

execute if data storage mgs:temp _base{mode:"zombies"} if data storage mgs:zombies game{map_id:"kino_der_toten"} run return run function mgs:v5.4.1/maps/zombies/kino_der_toten/leave

