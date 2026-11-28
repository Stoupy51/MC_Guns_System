
#> mgs:v5.4.4/lobby/missions/begin_round
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/missions/open_vote
#

scoreboard players set @a[scores={mgs.lobby.queue=3}] mgs.lobby.choice 0
function mgs:v5.4.4/lobby/missions/count_votes
scoreboard players set #lv_mi_dirty mgs.data 0
execute as @a[scores={mgs.lobby.queue=3}] at @s run playsound minecraft:block.note_block.pling ambient @s
execute as @a[scores={mgs.lobby.queue=3}] run function mgs:v5.4.4/lobby/missions/message

