
#> mgs:v5.0.0/sound/fire_alt
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/sound/main with storage mgs:gun all.sounds
#
# @args		fire_alt (unknown)
#

$playsound mgs:$(fire_alt) player @s ~ ~ ~ 0.25
$playsound mgs:$(fire_alt) player @a[distance=0.01..48] ~ ~ ~ 0.75 1 0.25

