
#> mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/tick
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/tick
#

# State 3: players in projection room — count down, then scatter to random lobby spots
execute if score #kino_tp_state mgs.data matches 3 run scoreboard players remove #kino_tp_timer mgs.data 1
execute if score #kino_tp_state mgs.data matches 3 if score #kino_tp_timer mgs.data matches ..0 run function mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/return_players

# State 4: players at random spots — count down 5s (100t), then tp all to lobby
execute if score #kino_tp_state mgs.data matches 4 run scoreboard players remove #kino_tp_timer mgs.data 1
execute if score #kino_tp_state mgs.data matches 4 if score #kino_tp_timer mgs.data matches ..0 run function mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/return_to_lobby

# State 5: cooldown — count down, then reset to idle (state 0)
execute if score #kino_tp_state mgs.data matches 5 run scoreboard players remove #kino_tp_cd mgs.data 1
execute if score #kino_tp_state mgs.data matches 5 if score #kino_tp_cd mgs.data matches ..0 run scoreboard players set #kino_tp_state mgs.data 0

