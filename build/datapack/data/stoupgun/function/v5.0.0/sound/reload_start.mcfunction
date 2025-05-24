
#> stoupgun:v5.0.0/sound/reload_start
#
# @within	stoupgun:v5.0.0/ammo/reload with storage stoupgun:gun all.stats
#

# Full reload sound for the player
$playsound stoupgun:$(base_weapon)/reload player @s ~ ~1000000 ~ 10000000

# Play the begin reload sound for all nearby players
$playsound stoupgun:$(base_weapon)/playerbegin player @a[distance=0.01..16] ~ ~ ~ 0.3

