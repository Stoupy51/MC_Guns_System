
#> mgs:v5.0.1/sound/fire_simple
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/sound/main with storage mgs:gun all.sounds
#
# @args		fire (unknown)
#

$playsound mgs:$(fire) player @s ~ ~ ~ 0.10
$playsound mgs:$(fire) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10

