
#> mgs:v5.0.0/sound/reload_start
#
# @within	mgs:v5.0.0/ammo/reload with storage mgs:gun all.stats
#

# Full reload sound for the player
$playsound mgs:$(base_weapon)/reload player

# Play the begin reload sound for all nearby players
$playsound mgs:$(base_weapon)/playerbegin player @a[distance=0.01..16] ~ ~ ~ 0.3

