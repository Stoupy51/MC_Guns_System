
#> mgs:v5.1.0/zombies/barricades/tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ at @s ]
#

# Run as the barricade display, at it.
execute if score @s mgs.zb.barricade.state matches 0 positioned ^ ^ ^-1 run function mgs:v5.1.0/zombies/barricades/intact_tick
execute if score @s mgs.zb.barricade.state matches 1 run function mgs:v5.1.0/zombies/barricades/destroyed_tick

# Pushes players out along the barricade's facing, in both states.
execute as @a[scores={mgs.zb.in_game=1},distance=..0.75] positioned as @s run tp @s ^ ^ ^0.8

# Same push for mannequins, so crawling players cannot clip through.
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,distance=..0.75] positioned as @s run tp @s ^ ^ ^0.8

