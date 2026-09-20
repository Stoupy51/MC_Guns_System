
#> mgs:v5.1.0/multiplayer/perks/tracker_footprint
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/perks/tracker_tick [ at @s ]
#

execute if score @s mgs.mp.team matches 1 run particle minecraft:dust{color:[0.95,0.85,0.2],scale:0.8} ~ ~0.1 ~ 0.15 0.02 0.15 0 3 force @a[scores={mgs.special.tracker=1..,mgs.mp.team=2}]
execute if score @s mgs.mp.team matches 2 run particle minecraft:dust{color:[0.95,0.85,0.2],scale:0.8} ~ ~0.1 ~ 0.15 0.02 0.15 0 3 force @a[scores={mgs.special.tracker=1..,mgs.mp.team=1}]
execute if score @s mgs.mp.team matches 0 run particle minecraft:dust{color:[0.95,0.85,0.2],scale:0.8} ~ ~0.1 ~ 0.15 0.02 0.15 0 3 force @a[scores={mgs.special.tracker=1..},distance=0.1..]

