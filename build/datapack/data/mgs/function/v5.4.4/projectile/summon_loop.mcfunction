
#> mgs:v5.4.4/projectile/summon_loop
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/player/fire_weapon
#			mgs:v5.4.4/projectile/summon_loop
#			mgs:v5.4.4/mob/fire_weapon
#

function mgs:v5.4.4/projectile/summon

scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.4.4/projectile/summon_loop

