
#> mgs:v5.4.4/lobby/multiplayer/begin_round
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/open_vote
#			mgs:v5.4.4/lobby/multiplayer/map_round
#

scoreboard players set @a[scores={mgs.lobby.queue=1}] mgs.lobby.choice 0
function mgs:v5.4.4/lobby/multiplayer/count_votes
scoreboard players set #lv_mp_dirty mgs.data 0
execute as @a[scores={mgs.lobby.queue=1}] at @s run playsound minecraft:block.note_block.pling ambient @s
execute as @a[scores={mgs.lobby.queue=1}] run function mgs:v5.4.4/lobby/multiplayer/message

