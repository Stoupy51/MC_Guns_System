
#> mgs:v5.1.0/maps/editor/tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# Only run for players in editor mode
execute unless score @s mgs.mp.map_edit matches 1 run return fail

# Actionbar: show nearest element info (within 5 blocks). Genuinely per-player, stays here.
tag @s add mgs.check_nearest
execute as @n[type=minecraft:marker,tag=mgs.map_element,distance=..5] run function mgs:v5.1.0/maps/editor/actionbar_nearest
tag @s remove mgs.check_nearest

# Everything else the editor draws is map-wide, not per-player, but this function runs once per
# editing player — so marker rotation syncing, the display rebuild and every particle used to be
# repeated for each of them. Do that work once per tick instead, whoever gets here first.
execute unless score #ed_global_tick mgs.data = #total_tick mgs.data run function mgs:v5.1.0/maps/editor/global_tick

