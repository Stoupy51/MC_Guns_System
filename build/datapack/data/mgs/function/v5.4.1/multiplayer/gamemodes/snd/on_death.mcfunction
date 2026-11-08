
#> mgs:v5.4.1/multiplayer/gamemodes/snd/on_death
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/enter_death_spectate
#

# First, while the carrier tag and its label still exist.
execute if entity @s[tag=mgs.snd_carrier] run function mgs:v5.4.1/multiplayer/gamemodes/snd/drop_bomb

# No respawn in S&D.
tag @s remove mgs.snd_alive
gamemode spectator @s

