
#> mgs:v5.0.0/sound/main
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# Fire sounds
# TODO: Add a mode check to select between fire and fire_alt
execute if data storage mgs:gun all.sounds.fire_alt run function mgs:v5.0.0/sound/fire_alt with storage mgs:gun all.sounds
execute unless data storage mgs:gun all.sounds.fire_alt run function mgs:v5.0.0/sound/fire_simple with storage mgs:gun all.sounds

# Acoustics handling
execute if data storage mgs:gun all.sounds.crack run function mgs:v5.0.0/sound/acoustics_main with storage mgs:gun all.sounds

