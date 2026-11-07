
#> mgs:v5.4.0/mob/fire_sound
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/mob/fire_weapon with storage mgs:gun all.sounds
#
# @args		fire (unknown)
#

$playsound mgs:$(fire) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10

