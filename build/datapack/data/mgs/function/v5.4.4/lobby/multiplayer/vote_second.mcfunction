
#> mgs:v5.4.4/lobby/multiplayer/vote_second
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/second
#

function mgs:v5.4.4/lobby/multiplayer/count_votes
execute if score #lv_mp_dirty mgs.data matches 1 as @a[scores={mgs.lobby.queue=1}] run function mgs:v5.4.4/lobby/multiplayer/message
scoreboard players set #lv_mp_dirty mgs.data 0

scoreboard players operation #lv_sec mgs.data = #lv_mp_timer mgs.data
scoreboard players operation #lv_sec mgs.data /= #20 mgs.data
scoreboard players add #lv_sec mgs.data 1
execute if score #lv_mp_round mgs.data matches 1 if score #lv_mp_voters mgs.data matches 0 run return run title @a[scores={mgs.lobby.queue=1}] actionbar {"translate":"mgs.the_countdown_starts_at_the_first_vote","fallback":"The countdown starts at the first vote.","color":"aqua"}
title @a[scores={mgs.lobby.queue=1}] actionbar [{"translate":"mgs.vote_ends_in","fallback":"Vote ends in ","color":"aqua"},{"score":{"name":"#lv_sec","objective":"mgs.data"},"color":"yellow"},{"text":" s","color":"aqua"}]

