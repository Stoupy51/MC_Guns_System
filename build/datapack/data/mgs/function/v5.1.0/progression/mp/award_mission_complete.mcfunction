
#> mgs:v5.1.0/progression/mp/award_mission_complete
#
# @executed	as @a[scores={mgs.mi.in_game=1}]
#
# @within	mgs:v5.1.0/missions/victory [ as @a[scores={mgs.mi.in_game=1}] ]
#

# Clearing a mission, to everyone still on the roster
scoreboard players add @s mgs.mp.xp_total 50
scoreboard players add @s mgs.mp.xp_prog 50
scoreboard players add @s mgs.mp.xp_session 50
function mgs:v5.1.0/progression/mp/settle

