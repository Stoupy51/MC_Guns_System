
#> mgs:v5.0.0/sound/cycle
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/sound/main with storage mgs:gun all.sounds
#
# @args		cycle (unknown)
#

$playsound mgs:$(cycle) player @s ~ ~ ~ 0.5
$playsound mgs:$(cycle) player @a[distance=0.01..48] ~ ~ ~ 1.0 1 0.5

