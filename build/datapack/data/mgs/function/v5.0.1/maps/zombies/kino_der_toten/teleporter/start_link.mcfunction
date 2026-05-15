
#> mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/start_link
#
# @executed	as @e[tag=mgs.kino]
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/on_theater_click
#

# State 1: theater clicked — waiting for the lobby pad to be clicked
scoreboard players set #kino_tp_state mgs.data 1
playsound minecraft:block.beacon.power_select block @a[distance=..50] ~ ~ ~ 1 1
tellraw @a[distance=..50] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.teleporter_link_started","color":"green"}]

