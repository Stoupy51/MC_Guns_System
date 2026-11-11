
#> mgs:v5.4.2/progression/mp/award_mission_complete
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/missions/victory [ as @a[scores={mgs.mi.in_game=1}] ]
#

# Clearing a mission, to everyone still on the roster
scoreboard players add @s mgs.mp.xp_total 50
scoreboard players add @s mgs.mp.xp_prog 50
scoreboard players add @s mgs.mp.xp_session 50
function mgs:v5.4.2/progression/mp/settle

