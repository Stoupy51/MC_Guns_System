
#> mgs:v5.4.4/sound/player_begin
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/ammo/reload with storage mgs:gun all.sounds
#
# @args		playerbegin (unknown)
#

$playsound mgs:$(playerbegin) player @a[distance=0.01..16] ~ ~ ~ 0.3

