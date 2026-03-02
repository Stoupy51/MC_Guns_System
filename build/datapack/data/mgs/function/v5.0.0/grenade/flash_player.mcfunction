
#> mgs:v5.0.0/grenade/flash_player
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/flash_check
#

# Apply full blindness + darkness
effect give @s minecraft:blindness 5 0 true
effect give @s minecraft:darkness 3 0 true

# White screen flash using custom font (1x1 white pixel scaled to fill screen)
title @s times 5 40 20
title @s title {"text":"F","font":"mgs:flash"}

