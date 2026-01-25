
#> mgs:v5.0.0/sound/reload_start
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/reload with storage mgs:gun all.sounds
#
# @args		reload (unknown)
#

# Full reload sound for the player
$playsound mgs:$(reload) player @s

