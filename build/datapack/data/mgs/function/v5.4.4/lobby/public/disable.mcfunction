
#> mgs:v5.4.4/lobby/public/disable
#
# @within	mgs:v5.4.4/dialog/close_then
#			dialog mgs:v5.4.4/config/global
#

scoreboard players set #public_lobby mgs.config 0
scoreboard players set #lv_mp_round mgs.data 0
scoreboard players set #lv_zb_round mgs.data 0
scoreboard players set #lv_mi_round mgs.data 0
scoreboard players reset * mgs.lobby.queue
scoreboard players reset * mgs.lobby.choice
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.public_lobby_off_games_running_go_on_queues_and_votes_are_cleare","fallback":"Public lobby off: games running go on, queues and votes are cleared.","color":"yellow"}]

