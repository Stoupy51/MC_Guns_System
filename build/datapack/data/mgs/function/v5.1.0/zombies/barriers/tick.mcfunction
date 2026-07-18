
#> mgs:v5.1.0/zombies/barriers/tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ at @s ]
#

# @s = barrier display, at @s — dispatch by state
execute if score @s mgs.zb.barrier.state matches 0 positioned ^ ^ ^-1 run function mgs:v5.1.0/zombies/barriers/intact_tick
execute if score @s mgs.zb.barrier.state matches 1 run function mgs:v5.1.0/zombies/barriers/destroyed_tick

# Player collision: push players in barrier's facing direction every tick (both states)
execute as @a[scores={mgs.zb.in_game=1},distance=..0.75] positioned as @s run tp @s ^ ^ ^0.8

# Downed mannequin collision: same push so crawling players can't clip through barriers
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,distance=..0.75] positioned as @s run tp @s ^ ^ ^0.8

