
#> mgs:v5.0.0/sound/fire_simple
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/sound/main with storage mgs:gun all.sounds
#
# @args		fire (unknown)
#

$playsound mgs:$(fire) player @s ~ ~ ~ 0.25
$playsound mgs:$(fire) player @a[distance=0.01..48] ~ ~ ~ 0.75 1 0.25

