
#> mgs:v5.0.0/sound/player_begin
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/reload with storage mgs:gun all.sounds
#
# @args		playerbegin (unknown)
#

# Play the begin reload sound for all nearby players
$playsound mgs:$(playerbegin) player @a[distance=0.01..16] ~ ~ ~ 0.3

