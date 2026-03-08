
#> mgs:v5.0.0/zombies/spectate_random_player
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/zombies/on_respawn
#

execute as @r[scores={mgs.zb.in_game=1},gamemode=!spectator] run spectate @s @p[scores={mgs.mp.spectate_timer=1..},sort=nearest]

