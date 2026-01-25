
#> mgs:v5.0.0/sound/pump
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/sound/check/pump with storage mgs:gun all.sounds
#
# @args		pump (unknown)
#

# Play the pump sound for the player and nearby players
$playsound mgs:$(pump) player @s
$playsound mgs:$(pump) player @a[distance=0.01..16] ~ ~ ~ 0.3

