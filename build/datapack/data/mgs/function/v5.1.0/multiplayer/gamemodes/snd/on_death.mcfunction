
#> mgs:v5.1.0/multiplayer/gamemodes/snd/on_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/enter_death_spectate
#

# First, while the carrier tag and its label still exist.
execute if entity @s[tag=mgs.snd_carrier] run function mgs:v5.1.0/multiplayer/gamemodes/snd/drop_bomb

# No respawn in S&D.
tag @s remove mgs.snd_alive
gamemode spectator @s

