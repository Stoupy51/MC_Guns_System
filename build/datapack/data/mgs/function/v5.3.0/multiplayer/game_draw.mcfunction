
#> mgs:v5.3.0/multiplayer/game_draw
#
# @within	mgs:v5.3.0/multiplayer/time_up
#			mgs:v5.3.0/multiplayer/gamemodes/demo/next_round
#

tellraw @a[scores={mgs.mp.in_game=1}] ["","🤝 ",{"translate":"mgs.draw","fallback":"Draw!","color":"gold","bold":true}]
function mgs:v5.3.0/multiplayer/stop

