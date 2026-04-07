
#> mgs:v5.0.0/ammo/decrease
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# If infinite ammo is active, refill ammo to max capacity and skip consumption
execute if score @s mgs.special.infinite_ammo matches 1.. run return run function mgs:v5.0.0/ammo/infinite_refill

# Remove 1 bullet from player's ammo count
scoreboard players remove @s mgs.remaining_bullets 1
execute if score @s mgs.remaining_bullets matches ..0 run function mgs:v5.0.0/ammo/reload

# Add mid cooldown sound tag if weapon has pump sound
execute if data storage mgs:gun all.sounds.pump run tag @s add mgs.pump_sound

# Add mid reload sound tag if weapon has reload mid sound
execute if data storage mgs:gun all.sounds.playermid run tag @s add mgs.reload_mid_sound

