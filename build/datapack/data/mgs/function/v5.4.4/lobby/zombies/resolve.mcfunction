
#> mgs:v5.4.4/lobby/zombies/resolve
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/zombies/vote_tick
#

scoreboard players set #lv_best mgs.data -1
scoreboard players set #lv_win mgs.data 1
execute if score #lv_zb_slots mgs.data matches 1.. run scoreboard players operation #lv_k mgs.data = #lv_zb_vote_1 mgs.data
execute if score #lv_zb_slots mgs.data matches 1.. run function mgs:v5.4.4/lobby/vote/weigh {slot:1}
execute if score #lv_zb_slots mgs.data matches 2.. run scoreboard players operation #lv_k mgs.data = #lv_zb_vote_2 mgs.data
execute if score #lv_zb_slots mgs.data matches 2.. run function mgs:v5.4.4/lobby/vote/weigh {slot:2}
execute if score #lv_zb_slots mgs.data matches 3.. run scoreboard players operation #lv_k mgs.data = #lv_zb_vote_3 mgs.data
execute if score #lv_zb_slots mgs.data matches 3.. run function mgs:v5.4.4/lobby/vote/weigh {slot:3}
execute if score #lv_zb_slots mgs.data matches 4.. run scoreboard players operation #lv_k mgs.data = #lv_zb_vote_4 mgs.data
execute if score #lv_zb_slots mgs.data matches 4.. run function mgs:v5.4.4/lobby/vote/weigh {slot:4}
execute if score #lv_zb_slots mgs.data matches 5.. run scoreboard players operation #lv_k mgs.data = #lv_zb_vote_5 mgs.data
execute if score #lv_zb_slots mgs.data matches 5.. run function mgs:v5.4.4/lobby/vote/weigh {slot:5}
execute if score #lv_zb_slots mgs.data matches 6.. run scoreboard players operation #lv_k mgs.data = #lv_zb_vote_6 mgs.data
execute if score #lv_zb_slots mgs.data matches 6.. run function mgs:v5.4.4/lobby/vote/weigh {slot:6}
execute if score #lv_zb_slots mgs.data matches 7.. run scoreboard players operation #lv_k mgs.data = #lv_zb_vote_7 mgs.data
execute if score #lv_zb_slots mgs.data matches 7.. run function mgs:v5.4.4/lobby/vote/weigh {slot:7}
execute if score #lv_zb_slots mgs.data matches 8.. run scoreboard players operation #lv_k mgs.data = #lv_zb_vote_8 mgs.data
execute if score #lv_zb_slots mgs.data matches 8.. run function mgs:v5.4.4/lobby/vote/weigh {slot:8}

data modify storage mgs:temp _lv_pick set value {mode:"zombies"}
scoreboard players remove #lv_win mgs.data 1
execute store result storage mgs:temp _lv_pick.i int 1 run scoreboard players get #lv_win mgs.data
function mgs:v5.4.4/lobby/vote/pick_winner with storage mgs:temp _lv_pick

# Random is the last slot: it draws one of the slots before it.
scoreboard players operation #lv_n mgs.data = #lv_zb_slots mgs.data
scoreboard players remove #lv_n mgs.data 2
execute store result storage mgs:temp _lv_pick.max int 1 run scoreboard players get #lv_n mgs.data
execute if data storage mgs:lobby zombies.winner.random run function mgs:v5.4.4/lobby/vote/pick_random with storage mgs:temp _lv_pick

tellraw @a[scores={mgs.lobby.queue=2}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.vote_result","fallback":"Vote result: ","color":"gray"},{"nbt":"zombies.winner.label","storage":"mgs:lobby","interpret":true}]
function mgs:v5.4.4/lobby/zombies/launch

