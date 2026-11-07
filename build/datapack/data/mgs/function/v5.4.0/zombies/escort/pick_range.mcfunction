
#> mgs:v5.4.0/zombies/escort/pick_range
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/escort/set_wander_target
#

execute if entity @s[distance=..24] run return run function mgs:v5.4.0/zombies/escort/set_range {range:48}
execute if entity @s[distance=..48] run return run function mgs:v5.4.0/zombies/escort/set_range {range:72}
function mgs:v5.4.0/zombies/escort/set_range {range:96}

