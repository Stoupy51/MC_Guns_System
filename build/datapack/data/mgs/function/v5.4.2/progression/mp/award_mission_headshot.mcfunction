
#> mgs:v5.4.2/progression/mp/award_mission_headshot
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/missions/xp/on_kill
#

# Added ON TOP of mission_kill, same doubling as the other two modes
scoreboard players add @s mgs.mp.xp_total 3
scoreboard players add @s mgs.mp.xp_prog 3
scoreboard players add @s mgs.mp.xp_session 3
function mgs:v5.4.2/progression/mp/settle

scoreboard players add @s mgs.st.mi.headshots 1

