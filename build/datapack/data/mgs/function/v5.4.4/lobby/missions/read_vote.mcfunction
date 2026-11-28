
#> mgs:v5.4.4/lobby/missions/read_vote
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/missions/vote_tick [ as @a[scores={mgs.lobby.queue=3,mgs.lobby.vote=1..}] ]
#

scoreboard players remove @s mgs.lobby.vote 30
execute if score @s mgs.lobby.vote matches 1.. if score @s mgs.lobby.vote <= #lv_mi_slots mgs.data run scoreboard players operation @s mgs.lobby.choice = @s mgs.lobby.vote
scoreboard players set @s mgs.lobby.vote 0
playsound minecraft:ui.button.click ambient @s

function mgs:v5.4.4/lobby/missions/count_votes
scoreboard players set #lv_mi_dirty mgs.data 1

