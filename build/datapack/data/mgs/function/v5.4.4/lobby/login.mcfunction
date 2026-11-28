
#> mgs:v5.4.4/lobby/login
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.4.4/player/tick
#			mgs:v5.4.4/dialog/close_then
#

scoreboard players operation #lv_away mgs.data = #now mgs.lobby.seen
scoreboard players operation #lv_away mgs.data -= @s mgs.lobby.seen
execute unless score @s mgs.lobby.seen matches -2147483648.. run scoreboard players set #lv_away mgs.data 601
scoreboard players operation @s mgs.lobby.seen = #now mgs.lobby.seen

scoreboard players set #lv_playing mgs.data 0
execute if score @s mgs.mp.in_game matches 1 unless data storage mgs:multiplayer game{state:"lobby"} run scoreboard players set #lv_playing mgs.data 1
execute if score @s mgs.zb.in_game matches 1 unless data storage mgs:zombies game{state:"lobby"} run scoreboard players set #lv_playing mgs.data 1
execute if score @s mgs.mi.in_game matches 1 unless data storage mgs:missions game{state:"lobby"} run scoreboard players set #lv_playing mgs.data 1
execute if score #lv_playing mgs.data matches 1 if score #lv_away mgs.data matches ..600 run return 0

# Away too long: out of the queue too. Back from a game that ended while away: still queued.
execute if score #lv_away mgs.data matches 601.. run scoreboard players set @s mgs.lobby.queue 0
function mgs:v5.4.4/lobby/leave_games
execute if score #lv_in_game mgs.data matches 0 run function mgs:v5.4.4/lobby/return

