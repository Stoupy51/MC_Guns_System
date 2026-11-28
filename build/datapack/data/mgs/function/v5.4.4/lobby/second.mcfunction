
#> mgs:v5.4.4/lobby/second
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/tick
#

scoreboard players set #lv_tick mgs.data 0
scoreboard players add #now mgs.lobby.seen 1
scoreboard players operation @a mgs.lobby.seen = #now mgs.lobby.seen

function mgs:v5.4.4/lobby/multiplayer/second
function mgs:v5.4.4/lobby/zombies/second
function mgs:v5.4.4/lobby/missions/second

