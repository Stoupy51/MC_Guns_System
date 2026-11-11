
#> mgs:v5.4.2/missions/spectate_random_player
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/missions/enter_death_spectate
#

execute as @r[scores={mgs.mi.in_game=1},gamemode=!spectator] run spectate @s @p[scores={mgs.mp.spectate_timer=1..},sort=nearest]

