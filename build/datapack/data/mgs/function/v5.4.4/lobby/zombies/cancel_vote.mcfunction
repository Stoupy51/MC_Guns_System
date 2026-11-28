
#> mgs:v5.4.4/lobby/zombies/cancel_vote
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/zombies/second
#

scoreboard players set #lv_zb_round mgs.data 0
scoreboard players set @a[scores={mgs.lobby.queue=2}] mgs.lobby.choice 0
tellraw @a[scores={mgs.lobby.queue=2}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.not_enough_players_left_the_vote_is_cancelled","fallback":"Not enough players left, the vote is cancelled.","color":"red"}]

