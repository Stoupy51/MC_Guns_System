
#> mgs:v5.4.2/multiplayer/perks/tracker_tick
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/game_tick
#

execute as @a[scores={mgs.mp.in_game=1},gamemode=!spectator] at @s run function mgs:v5.4.2/multiplayer/perks/tracker_footprint

