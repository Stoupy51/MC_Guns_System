
#> mgs:v5.4.2/multiplayer/end
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/game_tick
#

data modify storage mgs:multiplayer game.state set value "ended"
execute unless function mgs:v5.4.2/multiplayer/kill_cam/start run function mgs:v5.4.2/multiplayer/stop

