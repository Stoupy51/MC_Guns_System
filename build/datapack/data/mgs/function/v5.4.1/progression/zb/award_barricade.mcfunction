
#> mgs:v5.4.1/progression/zb/award_barricade
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/barricades/on_repair_complete_player
#

# Repairing a barricade; already capped at 25 repairs per round
scoreboard players add @s mgs.zb.xp_total 1
scoreboard players add @s mgs.zb.xp_prog 1
function mgs:v5.4.1/progression/zb/settle

scoreboard players add @s mgs.st.zb.barricades 1

