
#> mgs:v5.4.1/grenade/summon_loop
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/grenade/throw
#			mgs:v5.4.1/grenade/summon_loop
#

function mgs:v5.4.1/grenade/summon

scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.4.1/grenade/summon_loop

