
#> mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/return_to_lobby
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/tick
#

# Teleport all returning players to the lobby teleporter pad position
execute as @a[tag=mgs.kino.in_tp] at @e[tag=mgs.kino.teleporter_lobby] run tp @s ~ ~ ~
execute at @n[tag=mgs.kino.in_tp] run playsound minecraft:entity.enderman.teleport block @a[distance=..50] ~ ~ ~ 1 1
execute at @n[tag=mgs.kino.in_tp] run kill @e[tag=mgs.zombie_round,distance=..4]

# Clean up tags
tag @a remove mgs.kino.in_tp

# State 6: enter cooldown (1800t = 1m30)
scoreboard players set #kino_tp_state mgs.data 6
scoreboard players set #kino_tp_cd mgs.data 1800

