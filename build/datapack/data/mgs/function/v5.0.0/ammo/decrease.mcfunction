
#> mgs:v5.0.0/ammo/decrease
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# Remove 1 bullet from player's ammo count
scoreboard players remove @s mgs.remaining_bullets 1

# Add mid cooldown sound tag if weapon has pump sound
execute if data storage mgs:gun all.sounds.pump run tag @s add mgs.pump_sound

# Add mid reload sound tag if weapon has reload mid sound
execute if data storage mgs:gun all.sounds.playermid run tag @s add mgs.reload_mid_sound

