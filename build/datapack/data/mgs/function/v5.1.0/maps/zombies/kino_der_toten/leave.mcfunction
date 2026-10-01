
#> mgs:v5.1.0/maps/zombies/kino_der_toten/leave
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/calls/leave
#

kill @e[tag=mgs.kino]

tag @a remove mgs.kino.in_tp

scoreboard players set #kino_tp_state mgs.data 0
scoreboard players set #kino_tp_timer mgs.data 0
scoreboard players set #kino_tp_cd mgs.data 0
scoreboard players set #kino_met_count mgs.data 0

