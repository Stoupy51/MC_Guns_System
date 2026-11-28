
#> mgs:v5.4.4/lobby/multiplayer/leave
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/leave_games
#

function mgs:v5.4.4/shared/maps/call_script_at_base {mode:"multiplayer",script:"leave"}
function mgs:v5.4.4/multiplayer/reset_player
tellraw @a[scores={mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"selector":"@s"},[{"text":" ","color":"gray"}, {"translate":"mgs.went_back_to_the_lobby","fallback":"went back to the lobby."}]]
execute unless entity @a[scores={mgs.mp.in_game=1}] unless data storage mgs:multiplayer game{state:"lobby"} run function mgs:v5.4.4/multiplayer/stop

