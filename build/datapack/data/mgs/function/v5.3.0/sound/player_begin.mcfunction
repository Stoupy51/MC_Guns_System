
#> mgs:v5.3.0/sound/player_begin
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/ammo/reload with storage mgs:gun all.sounds
#
# @args		playerbegin (unknown)
#

$playsound mgs:$(playerbegin) player @a[distance=0.01..16] ~ ~ ~ 0.3

