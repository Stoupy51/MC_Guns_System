
#> mgs:v5.4.2/stats/mi/on_mission_end
#
# @within	#mgs:missions/on_mission_end
#			mgs:v5.4.2/dialog/close_then
#

execute if score #mi_timer mgs.data matches 1.. run scoreboard players add @a[scores={mgs.mi.in_game=1}] mgs.st.mi.games 1
function mgs:v5.4.2/stats/mi/game_end

scoreboard players set #st_mi_won mgs.data 0

