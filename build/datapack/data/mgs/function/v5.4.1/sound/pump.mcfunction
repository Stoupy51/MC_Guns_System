
#> mgs:v5.4.1/sound/pump
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/sound/check/pump with storage mgs:gun all.sounds
#
# @args		pump (unknown)
#

$playsound mgs:$(pump) player @s
$playsound mgs:$(pump) player @a[distance=0.01..16] ~ ~ ~ 0.3

