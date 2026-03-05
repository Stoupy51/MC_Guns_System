
#> mgs:v5.0.0/multiplayer/gamemodes/dom/point_particles
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/dom/tick [ at @s ]
#

# Neutral = white, red = red, blue = blue
execute if score @s mgs.mp.dom_owner matches 0 run particle dust{color:[1.0,1.0,1.0],scale:1.0} ~ ~1 ~ 1.5 0.5 1.5 0 5
execute if score @s mgs.mp.dom_owner matches 1 run particle dust{color:[1.0,0.2,0.2],scale:1.0} ~ ~1 ~ 1.5 0.5 1.5 0 5
execute if score @s mgs.mp.dom_owner matches 2 run particle dust{color:[0.2,0.2,1.0],scale:1.0} ~ ~1 ~ 1.5 0.5 1.5 0 5

