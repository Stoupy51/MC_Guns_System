
#> mgs:v5.1.0/maps/editor/tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

execute unless score @s mgs.mp.map_edit matches 1 run return fail

# Nearest element within 5 blocks; genuinely per player.
tag @s add mgs.check_nearest
execute as @n[type=minecraft:marker,tag=mgs.map_element,distance=..5] run function mgs:v5.1.0/maps/editor/actionbar_nearest
tag @s remove mgs.check_nearest

# Everything else is map-wide but this runs per editing player, so it is done once per tick, by whoever gets here first.
execute unless score #ed_global_tick mgs.data = #total_tick mgs.data run function mgs:v5.1.0/maps/editor/global_tick

