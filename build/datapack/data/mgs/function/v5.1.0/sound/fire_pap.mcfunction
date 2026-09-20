
#> mgs:v5.1.0/sound/fire_pap
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/sound/main with storage mgs:gun all.sounds
#
# @args		pap_fire (unknown)
#

$playsound mgs:$(pap_fire) player @s ~ ~ ~ 0.10
$playsound mgs:$(pap_fire) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10

