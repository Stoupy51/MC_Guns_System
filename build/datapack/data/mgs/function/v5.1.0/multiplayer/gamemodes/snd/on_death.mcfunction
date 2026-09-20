
#> mgs:v5.1.0/multiplayer/gamemodes/snd/on_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/enter_death_spectate
#

# Drop the bomb before anything else, while the carrier tag and its label are still around
execute if entity @s[tag=mgs.snd_carrier] run function mgs:v5.1.0/multiplayer/gamemodes/snd/drop_bomb

# Remove alive tag (no respawn in S&D)
tag @s remove mgs.snd_alive
# Set to spectator mode
gamemode spectator @s

