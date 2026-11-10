
#> mgs:v5.4.1/multiplayer/game_draw
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/time_up
#			mgs:v5.4.1/multiplayer/gamemodes/demo/next_round
#

tellraw @a[scores={mgs.mp.in_game=1}] ["","🤝 ",{"translate":"mgs.draw","fallback":"Draw!","color":"gold","bold":true}]
function mgs:v5.4.1/multiplayer/request_end

