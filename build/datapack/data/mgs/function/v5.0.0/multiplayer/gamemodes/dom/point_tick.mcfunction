
#> mgs:v5.0.0/multiplayer/gamemodes/dom/point_tick
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/dom/tick [ at @s ]
#

# Count red and blue players within 5 blocks
execute store result score #_dom_red mgs.data if entity @a[distance=..5,scores={mgs.mp.team=1}]
execute store result score #_dom_blue mgs.data if entity @a[distance=..5,scores={mgs.mp.team=2}]

# If contested (both teams present), no progress change
execute if score #_dom_red mgs.data matches 1.. if score #_dom_blue mgs.data matches 1.. run return fail

# If only red present: progress toward red (increase toward 100)
execute if score #_dom_red mgs.data matches 1.. unless score #_dom_blue mgs.data matches 1.. run function mgs:v5.0.0/multiplayer/gamemodes/dom/capture_red

# If only blue present: progress toward blue (decrease toward -100)
execute if score #_dom_blue mgs.data matches 1.. unless score #_dom_red mgs.data matches 1.. run function mgs:v5.0.0/multiplayer/gamemodes/dom/capture_blue

