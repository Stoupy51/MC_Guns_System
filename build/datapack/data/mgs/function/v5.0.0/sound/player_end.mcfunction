
#> mgs:v5.0.0/sound/player_end
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/sound/check/reload_end with storage mgs:gun all.sounds
#
# @args		playerend (unknown)
#

# Play the end reload sound for all nearby players
$playsound mgs:$(playerend) player @a[distance=0.01..16] ~ ~ ~ 0.3

