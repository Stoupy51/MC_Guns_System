
#> mgs:v5.1.0/multiplayer/gamemodes/snd/on_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/enter_death_spectate
#

# Remove alive tag (no respawn in S&D)
tag @s remove mgs.snd_alive
# Set to spectator mode
gamemode spectator @s

