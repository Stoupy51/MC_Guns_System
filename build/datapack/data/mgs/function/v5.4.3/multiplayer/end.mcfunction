
#> mgs:v5.4.3/multiplayer/end
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/multiplayer/game_tick
#

data modify storage mgs:multiplayer game.state set value "ended"
execute unless function mgs:v5.4.3/multiplayer/kill_cam/start run function mgs:v5.4.3/multiplayer/stop

