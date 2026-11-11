
#> mgs:v5.4.2/projectile/summon_loop
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/fire_weapon
#			mgs:v5.4.2/projectile/summon_loop
#			mgs:v5.4.2/mob/fire_weapon
#

function mgs:v5.4.2/projectile/summon

scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.4.2/projectile/summon_loop

