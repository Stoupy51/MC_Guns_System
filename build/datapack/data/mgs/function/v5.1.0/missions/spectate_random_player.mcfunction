
#> mgs:v5.1.0/missions/spectate_random_player
#
# @executed	at @s
#
# @within	mgs:v5.1.0/missions/enter_death_spectate
#

# Pick a random alive in-game player (not self, not spectator)
execute as @r[scores={mgs.mi.in_game=1},gamemode=!spectator] run spectate @s @p[scores={mgs.mp.spectate_timer=1..},sort=nearest]

