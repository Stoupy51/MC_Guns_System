
#> mgs:v5.0.1/multiplayer/spectate_random_player
#
# @executed	at @s
#
# @within	mgs:v5.0.1/multiplayer/simulate_death
#			mgs:v5.0.1/multiplayer/on_respawn
#

# Pick a random alive in-game player (not self, not spectator)
execute as @r[scores={mgs.mp.in_game=1},gamemode=!spectator] run spectate @s @p[scores={mgs.mp.spectate_timer=1..},sort=nearest]

