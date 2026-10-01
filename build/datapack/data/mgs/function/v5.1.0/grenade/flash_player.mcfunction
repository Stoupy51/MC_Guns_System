
#> mgs:v5.1.0/grenade/flash_player
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/flash_check
#

# Tactical Mask (MP): short blindness, no darkness, a brief screen flash.
execute if score @s mgs.mp.in_game matches 1 if score @s mgs.special.tactical_mask matches 1 run return run function mgs:v5.1.0/grenade/flash_player_masked

effect give @s minecraft:blindness 5 0 true
effect give @s minecraft:darkness 3 0 true

# A custom font pixel scaled to fill the screen.
title @s times 5 40 20
title @s title {"text":"F","font":"mgs:flash"}

