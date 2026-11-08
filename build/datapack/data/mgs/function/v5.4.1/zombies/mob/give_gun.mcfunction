
#> mgs:v5.4.1/zombies/mob/give_gun
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/mob/arm with storage mgs:temp _mob.gun
#
# @args		id (unknown)
#

$loot replace entity @s weapon.mainhand loot mgs:i/$(id)

