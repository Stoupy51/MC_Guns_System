
#> mgs:v5.0.0/sound/reload_end
#
# @within	mgs:v5.0.0/sound/check_reload_end with storage mgs:gun all.stats
#

# Play the end reload sound for all nearby players
$playsound mgs:$(base_weapon)/playerend player @a[distance=0.01..16] ~ ~ ~ 0.3

