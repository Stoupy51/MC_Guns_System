
#> mgs:v5.4.4/multiplayer/spectate_random_player
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/multiplayer/enter_death_spectate
#

execute as @r[scores={mgs.mp.in_game=1},gamemode=!spectator] run spectate @s @p[scores={mgs.mp.spectate_timer=1..},sort=nearest]

