
#> mgs:v5.0.0/multiplayer/gamemodes/dom/point_particles
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/dom/tick [ at @s ]
#

# Base ring around zone
scoreboard players add @s mgs.mp.dom_owner 0
execute if score @s mgs.mp.dom_owner matches 0 run particle dust{color:[1.0,1.0,1.0],scale:1.5} ~ ~0.5 ~ 2.5 0.3 2.5 0 10
execute if score @s mgs.mp.dom_owner matches 1 run particle dust{color:[1.0,0.2,0.2],scale:1.5} ~ ~0.5 ~ 2.5 0.3 2.5 0 10
execute if score @s mgs.mp.dom_owner matches 2 run particle dust{color:[0.2,0.2,1.0],scale:1.5} ~ ~0.5 ~ 2.5 0.3 2.5 0 10

# Vertical beam (visible from distance)
execute if score @s mgs.mp.dom_owner matches 0 run particle dust{color:[1.0,1.0,1.0],scale:2.0} ~ ~8 ~ 0.1 2.0 0.1 0 3
execute if score @s mgs.mp.dom_owner matches 1 run particle dust{color:[1.0,0.2,0.2],scale:2.0} ~ ~8 ~ 0.1 2.0 0.1 0 3
execute if score @s mgs.mp.dom_owner matches 2 run particle dust{color:[0.2,0.2,1.0],scale:2.0} ~ ~8 ~ 0.1 2.0 0.1 0 3

