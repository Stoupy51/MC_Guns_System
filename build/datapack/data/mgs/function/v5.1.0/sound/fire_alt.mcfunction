
#> mgs:v5.1.0/sound/fire_alt
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/sound/main with storage mgs:gun all.sounds
#
# @args		fire_alt (unknown)
#

$playsound mgs:$(fire_alt) player @s ~ ~ ~ 0.10
$playsound mgs:$(fire_alt) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10

