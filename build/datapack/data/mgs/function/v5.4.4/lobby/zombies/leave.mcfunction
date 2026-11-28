
#> mgs:v5.4.4/lobby/zombies/leave
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/leave_games
#

function mgs:v5.4.4/zombies/reset_player
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"selector":"@s"},[{"text":" ","color":"gray"}, {"translate":"mgs.went_back_to_the_lobby","fallback":"went back to the lobby."}]]
execute unless entity @a[scores={mgs.zb.in_game=1}] unless data storage mgs:zombies game{state:"lobby"} run function mgs:v5.4.4/zombies/stop

