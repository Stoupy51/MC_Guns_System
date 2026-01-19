
#> mgs:v5.0.0/sound/reload_start
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/reload with storage mgs:gun all.sounds
#
# @args		reload (unknown)
#			playerbegin (unknown)
#

# Full reload sound for the player
$playsound mgs:$(reload) player

# Play the begin reload sound for all nearby players
$playsound mgs:$(playerbegin) player @a[distance=0.01..16] ~ ~ ~ 0.3

