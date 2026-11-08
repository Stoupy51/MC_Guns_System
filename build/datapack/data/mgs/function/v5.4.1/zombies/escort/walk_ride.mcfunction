
#> mgs:v5.4.1/zombies/escort/walk_ride
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/escort/zombie_tick
#

scoreboard players set #zb_esc_arrived mgs.data 0
function mgs:v5.4.1/zombies/escort/check_walk_arrived with entity @s data.walk_to
execute if score #zb_esc_arrived mgs.data matches 1 run return run function mgs:v5.4.1/zombies/escort/release

function mgs:v5.4.1/zombies/escort/escort_tail

