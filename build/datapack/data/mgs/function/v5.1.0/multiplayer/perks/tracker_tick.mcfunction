
#> mgs:v5.1.0/multiplayer/perks/tracker_tick
#
# @within	mgs:v5.1.0/multiplayer/game_tick
#

execute as @a[scores={mgs.mp.in_game=1},gamemode=!spectator] at @s run function mgs:v5.1.0/multiplayer/perks/tracker_footprint

