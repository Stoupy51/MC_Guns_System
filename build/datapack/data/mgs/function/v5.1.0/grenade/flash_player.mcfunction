
#> mgs:v5.1.0/grenade/flash_player
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.1.0/grenade/flash_check
#

# Tactical Mask perk (MP): greatly reduced flash — short blindness, no darkness, brief screen
execute if score @s mgs.mp.in_game matches 1 if score @s mgs.special.tactical_mask matches 1 run return run function mgs:v5.1.0/grenade/flash_player_masked

# Apply full blindness + darkness
effect give @s minecraft:blindness 5 0 true
effect give @s minecraft:darkness 3 0 true

# White screen flash using custom font (1x1 white pixel scaled to fill screen)
title @s times 5 40 20
title @s title {"text":"F","font":"mgs:flash"}

