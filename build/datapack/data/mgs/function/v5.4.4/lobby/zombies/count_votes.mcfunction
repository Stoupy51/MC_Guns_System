
#> mgs:v5.4.4/lobby/zombies/count_votes
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/zombies/begin_round
#			mgs:v5.4.4/lobby/zombies/read_vote
#			mgs:v5.4.4/lobby/zombies/vote_second
#

execute store result score #lv_zb_vote_1 mgs.data if entity @a[scores={mgs.lobby.queue=2,mgs.lobby.choice=1}]
execute store result score #lv_zb_vote_2 mgs.data if entity @a[scores={mgs.lobby.queue=2,mgs.lobby.choice=2}]
execute store result score #lv_zb_vote_3 mgs.data if entity @a[scores={mgs.lobby.queue=2,mgs.lobby.choice=3}]
execute store result score #lv_zb_vote_4 mgs.data if entity @a[scores={mgs.lobby.queue=2,mgs.lobby.choice=4}]
execute store result score #lv_zb_vote_5 mgs.data if entity @a[scores={mgs.lobby.queue=2,mgs.lobby.choice=5}]
execute store result score #lv_zb_vote_6 mgs.data if entity @a[scores={mgs.lobby.queue=2,mgs.lobby.choice=6}]
execute store result score #lv_zb_vote_7 mgs.data if entity @a[scores={mgs.lobby.queue=2,mgs.lobby.choice=7}]
execute store result score #lv_zb_vote_8 mgs.data if entity @a[scores={mgs.lobby.queue=2,mgs.lobby.choice=8}]
execute store result score #lv_zb_voters mgs.data if entity @a[scores={mgs.lobby.queue=2,mgs.lobby.choice=1..}]

