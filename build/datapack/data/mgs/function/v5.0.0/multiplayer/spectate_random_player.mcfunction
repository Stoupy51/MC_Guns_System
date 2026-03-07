
#> mgs:v5.0.0/multiplayer/spectate_random_player
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/multiplayer/simulate_death
#			mgs:v5.0.0/multiplayer/on_respawn
#

# Pick a random alive in-game player (not self, not spectator)
execute as @a[scores={mgs.mp.in_game=1},gamemode=!spectator,sort=random,limit=1] run spectate @s @p[scores={mgs.mp.spectate_timer=1..},sort=nearest]

