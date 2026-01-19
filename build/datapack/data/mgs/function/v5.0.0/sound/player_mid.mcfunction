
#> mgs:v5.0.0/sound/player_mid
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/sound/check/reload_mid with storage mgs:gun all.sounds
#
# @args		playermid (unknown)
#

# Play the mid reload sound for all nearby players
$playsound mgs:$(playermid) player @a[distance=0.01..16] ~ ~ ~ 0.3

