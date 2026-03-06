
#> mgs:v5.0.0/multiplayer/gamemodes/snd/on_death
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/on_respawn
#

# Remove alive tag (no respawn in S&D)
tag @s remove mgs.snd_alive
# Set to spectator mode
gamemode spectator @s

