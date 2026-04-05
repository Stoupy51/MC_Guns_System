
#> mgs:v5.0.0/multiplayer/gamemodes/dom/point_tick
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/dom/tick [ at @s ]
#

# Visual capture progress particles (smooth blue <-> yellow <-> red gradient)
execute if score @s mgs.mp.dom_progress matches -65..65 run particle dust{color:[1.0,1.0,0.0],scale:1.0} ~ ~1 ~ 1 1 1 0 5
execute if score @s mgs.mp.dom_progress matches 34..65 run particle dust{color:[1.0,0.75,0.25],scale:1.0} ~ ~1 ~ 1 1 1 0 5
execute if score @s mgs.mp.dom_progress matches 66..99 run particle dust{color:[1.0,0.5,0.0],scale:1.0} ~ ~1 ~ 1 1 1 0 5
execute if score @s mgs.mp.dom_progress matches 100 run particle dust{color:[1.0,0.0,0.0],scale:1.0} ~ ~1 ~ 1 1 1 0 5
execute if score @s mgs.mp.dom_progress matches -65..-34 run particle dust{color:[0.25,0.75,1.0],scale:1.0} ~ ~1 ~ 1 1 1 0 5
execute if score @s mgs.mp.dom_progress matches -99..-66 run particle dust{color:[0.0,0.5,1.0],scale:1.0} ~ ~1 ~ 1 1 1 0 5
execute if score @s mgs.mp.dom_progress matches -100 run particle dust{color:[0.0,0.0,1.0],scale:1.0} ~ ~1 ~ 1 1 1 0 5

# Count red and blue players within 5 blocks
execute store result score #dom_red mgs.data if entity @a[distance=..5,gamemode=!spectator,scores={mgs.mp.in_game=1,mgs.mp.team=1}]
execute store result score #dom_blue mgs.data if entity @a[distance=..5,gamemode=!spectator,scores={mgs.mp.in_game=1,mgs.mp.team=2}]

# If contested (both teams present), no progress change
execute if score #dom_red mgs.data matches 1.. if score #dom_blue mgs.data matches 1.. run return fail

# If only red present: progress toward red (increase toward 100)
execute if score #dom_red mgs.data matches 1.. unless score #dom_blue mgs.data matches 1.. run function mgs:v5.0.0/multiplayer/gamemodes/dom/capture_red

# If only blue present: progress toward blue (decrease toward -100)
execute if score #dom_blue mgs.data matches 1.. unless score #dom_red mgs.data matches 1.. run function mgs:v5.0.0/multiplayer/gamemodes/dom/capture_blue

