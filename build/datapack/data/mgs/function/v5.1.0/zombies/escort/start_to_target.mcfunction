
#> mgs:v5.1.0/zombies/escort/start_to_target
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/zombie_finish_rise
#

execute if score #zb_escort_count mgs.data matches 16.. run return 0
scoreboard players set #zb_escort_mode mgs.data 2
function mgs:v5.1.0/zombies/escort/start

