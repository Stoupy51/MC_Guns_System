
#> mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/tick
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/tick
#

# State 3: build-up, then teleport.
execute if score #kino_tp_state mgs.data matches 3 at @e[tag=mgs.kino.teleporter_theater] run function mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/activating_tick

# States 4 to 6 count down in real time (#tick_delta), so one-shot cues fire when the timer crosses a threshold,
# not on an exact value a delta of 2+ could skip. State 4: projection room, then scatter to random lobby spots.
execute if score #kino_tp_state mgs.data matches 4 run scoreboard players operation #kino_prev_t mgs.data = #kino_tp_timer mgs.data
execute if score #kino_tp_state mgs.data matches 4 run scoreboard players operation #kino_tp_timer mgs.data -= #tick_delta mgs.data
execute if score #kino_tp_state mgs.data matches 4 if score #kino_prev_t mgs.data matches 31.. if score #kino_tp_timer mgs.data matches ..30 as @a[tag=mgs.kino.in_tp] at @s run playsound minecraft:block.portal.trigger block @a[distance=..50] ~ ~ ~ 1 2
execute if score #kino_tp_state mgs.data matches 4 if score #kino_tp_timer mgs.data matches ..0 run function mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/return_players

# State 5: 5 s at the random spots, then everyone to the lobby pad.
execute if score #kino_tp_state mgs.data matches 5 run scoreboard players operation #kino_prev_t mgs.data = #kino_tp_timer mgs.data
execute if score #kino_tp_state mgs.data matches 5 run scoreboard players operation #kino_tp_timer mgs.data -= #tick_delta mgs.data
execute if score #kino_tp_state mgs.data matches 5 if score #kino_prev_t mgs.data matches 31.. if score #kino_tp_timer mgs.data matches ..30 as @a[tag=mgs.kino.in_tp] at @s run playsound minecraft:block.portal.trigger block @a[distance=..50] ~ ~ ~ 1 2
execute if score #kino_tp_state mgs.data matches 5 if score #kino_tp_timer mgs.data matches ..0 run function mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/return_to_lobby

# State 6: cooldown, then idle.
execute if score #kino_tp_state mgs.data matches 6 run scoreboard players operation #kino_prev_t mgs.data = #kino_tp_cd mgs.data
execute if score #kino_tp_state mgs.data matches 6 run scoreboard players operation #kino_tp_cd mgs.data -= #tick_delta mgs.data
execute if score #kino_tp_state mgs.data matches 6 if score #kino_prev_t mgs.data matches 2.. if score #kino_tp_cd mgs.data matches ..1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_teleporter_is_ready_to_use_again","color":"green"}]
execute if score #kino_tp_state mgs.data matches 6 if score #kino_tp_cd mgs.data matches ..0 run scoreboard players set #kino_tp_state mgs.data 0

