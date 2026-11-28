
#> mgs:v5.4.4/lobby/zombies/begin_round
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/zombies/open_vote
#

scoreboard players set @a[scores={mgs.lobby.queue=2}] mgs.lobby.choice 0
function mgs:v5.4.4/lobby/zombies/count_votes
scoreboard players set #lv_zb_dirty mgs.data 0
execute as @a[scores={mgs.lobby.queue=2}] at @s run playsound minecraft:block.note_block.pling ambient @s
execute as @a[scores={mgs.lobby.queue=2}] run function mgs:v5.4.4/lobby/zombies/message

