
#> mgs:v5.4.1/player/stamina_bar
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/stamina_tick
#

effect clear @s minecraft:saturation
effect clear @s minecraft:hunger

# Refill only below target, never at or above, so the invisible saturation cannot stack past what is shown.
execute if score @s mgs.food < #stam_t mgs.data run return run function mgs:v5.4.1/player/stamina_refill
execute if score @s mgs.food > #stam_t mgs.data run return run function mgs:v5.4.1/player/stamina_burn

# At target, burning the estimated leftover makes the next drain show at once.
execute if score @s mgs.stam_sat matches 1.. run function mgs:v5.4.1/player/stamina_burn

