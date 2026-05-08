
#> mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/return_to_lobby
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/tick
#

# Teleport all returning players to the lobby teleporter pad position
execute as @a[tag=mgs.kino.in_tp] at @e[tag=mgs.kino.teleporter_lobby] run tp @s ~ ~ ~

# Clean up tags
tag @a remove mgs.kino.in_tp

# State 5: enter cooldown (3600t = 3 min)
scoreboard players set #kino_tp_state mgs.data 5
scoreboard players set #kino_tp_cd mgs.data 3600

