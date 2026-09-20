
#> mgs:v5.1.0/zombies/escort/walk_ride
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/zombie_tick
#

scoreboard players set #zb_esc_arrived mgs.data 0
function mgs:v5.1.0/zombies/escort/check_walk_arrived with entity @s data.walk_to
execute if score #zb_esc_arrived mgs.data matches 1 run return run function mgs:v5.1.0/zombies/escort/release

function mgs:v5.1.0/zombies/escort/escort_tail

