
#> mgs:v5.4.4/lobby/send_home
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/player/config/process
#

execute unless score #public_lobby mgs.config matches 1 run return fail
scoreboard players set @s mgs.lobby.queue 0
function mgs:v5.4.4/lobby/leave_games
execute if score #lv_in_game mgs.data matches 0 run function mgs:v5.4.4/lobby/return

