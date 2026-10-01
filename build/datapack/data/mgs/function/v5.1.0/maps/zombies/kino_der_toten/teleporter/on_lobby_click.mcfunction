
#> mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/on_lobby_click
#
# @executed	as @e[tag=mgs.kino]
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/on_right_click
#

execute unless score #kino_tp_state mgs.data matches 1 run return fail

# State 2 (armed): the next theater click teleports.
scoreboard players set #kino_tp_state mgs.data 2
playsound minecraft:block.beacon.activate block @a[distance=..50] ~ ~ ~ 1 1
tellraw @a[distance=..50] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.teleporter_linked_click_the_theater_pad_again_to_teleport","color":"green"}]

