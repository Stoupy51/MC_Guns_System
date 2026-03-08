
#> mgs:v5.0.0/zombies/mystery_box/on_interact
#
# @executed	as @e[tag=mgs.mystery_box_active]
#
# @within	mgs:v5.0.0/zombies/mystery_box/check_use [ as @e[tag=mgs.mystery_box_active] ]
#

# @s = mystery box interaction entity
# Clear interaction data
data remove entity @s interaction

# Run as the nearest player (must be within interaction range)
execute as @p[distance=..3,scores={mgs.zb.in_game=1}] run function mgs:v5.0.0/zombies/mystery_box/try_use

