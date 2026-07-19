
#> mgs:v5.1.0/zombies/admin/round_skip_1
#
# @within	???
#

execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_zombies_game_is_active","color":"red"}]
execute store result score #zb_round mgs.data run data get storage mgs:zombies game.round
scoreboard players add #zb_round mgs.data 0
execute store result storage mgs:zombies game.round int 1 run scoreboard players get #zb_round mgs.data
function mgs:v5.1.0/zombies/admin/force_round_end
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.an_operator_skipped_ahead_1_rounds","color":"yellow"}]

