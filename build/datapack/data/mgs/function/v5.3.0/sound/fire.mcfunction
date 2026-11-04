
#> mgs:v5.3.0/sound/fire
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/sound/main with storage mgs:temp fire_sound
#
# @args		self (unknown)
#			others (unknown)
#

$playsound mgs:$(self) player @s ~ ~ ~ 0.10
$playsound mgs:$(others) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10

