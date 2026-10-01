
#> mgs:v5.1.0/ammo/decrease
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/right_click
#

# Infinite ammo refills to capacity and consumes nothing.
execute if score @s mgs.special.infinite_ammo matches 1.. run return run function mgs:v5.1.0/ammo/infinite_refill

scoreboard players remove @s mgs.remaining_bullets 1
execute if score @s mgs.remaining_bullets matches ..0 run function mgs:v5.1.0/ammo/reload

# Read by the mid-cooldown sound check.
execute if data storage mgs:gun all.sounds.pump run tag @s add mgs.pump_sound

# Read by the mid-reload sound check.
execute if data storage mgs:gun all.sounds.playermid run tag @s add mgs.reload_mid_sound

