
#> mgs:v5.4.1/sound/cycle
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/sound/main with storage mgs:gun all.sounds
#
# @args		cycle (unknown)
#

$playsound mgs:$(cycle) player @s ~ ~ ~ 0.5
$playsound mgs:$(cycle) player @a[distance=0.01..48] ~ ~ ~ 1.0 1 0.5

