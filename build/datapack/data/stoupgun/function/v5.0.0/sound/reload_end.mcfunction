
#> stoupgun:v5.0.0/sound/reload_end
#
# @within	stoupgun:v5.0.0/sound/check_reload_end with storage stoupgun:gun all.stats
#

# Play the end reload sound for all nearby players
$playsound stoupgun:$(base_weapon)/playerend player @a[distance=0.01..16] ~ ~ ~ 0.3

# Remove reloading tag
tag @s remove stoupgun.reloading

