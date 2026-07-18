
#> mgs:v5.1.0/mob/fire_sound
#
# @executed	anchored eyes & facing entity @e[tag=mgs.target,limit=1] feet
#
# @within	mgs:v5.1.0/mob/fire_weapon with storage mgs:gun all.sounds
#
# @args		fire (unknown)
#

$playsound mgs:$(fire) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10

