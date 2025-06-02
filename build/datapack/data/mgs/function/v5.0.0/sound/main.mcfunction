
#> mgs:v5.0.0/sound/main
#
# @within	mgs:v5.0.0/player/right_click with storage mgs:gun all.stats
#

# Simple weapon fire sound
$playsound mgs:$(base_weapon)/fire player @s ~ ~ ~ 0.25
$playsound mgs:$(base_weapon)/fire player @a[distance=0.01..48] 0.75 1 0.25

# Compute acoustics, and playsound
function mgs:v5.0.0/sound/acoustics with storage mgs:gun all.stats

