
#> mgs:v5.1.0/progression/adv/mp/level/reward_7
#
# @executed	as the player & at current position
#
# @within	advancement mgs:challenges/mp/level_7
#

# Rank 100: 250 XP into the mp pool
scoreboard players operation #adv_gain_prev mgs.data = #xp_gain mgs.data
scoreboard players set #xp_gain mgs.data 250
tag @s add mgs.xp_earner
tellraw @a[tag=!mgs.xp_earner] {"text":"","hover_event":{"action":"show_text","value":[[{"translate":"mgs.rank","color":"yellow"}, " 100"],"\n",[{"translate":"mgs.reach_multiplayer_level","color":"gray"}, " 100"]]},"extra":[[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"🏆 ","color":"white"},["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"yellow"}],[{"text":" ","color":"gray"}, {"translate":"mgs.unlocked_challenge"}],[{"translate":"mgs.rank","color":"yellow"}, " 100"]]}
tag @s remove mgs.xp_earner
tellraw @s {"text":"","hover_event":{"action":"show_text","value":[[{"translate":"mgs.rank","color":"yellow"}, " 100"],"\n",[{"translate":"mgs.reach_multiplayer_level","color":"gray"}, " 100"]]},"extra":[[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"🏆 ","color":"white"},{"translate":"mgs.challenge_unlocked","color":"gray"},[{"translate":"mgs.rank","color":"yellow"}, " 100"],[" ",{"text":"+","color":"gold"},{"score":{"name":"#xp_gain","objective":"mgs.data"},"color":"gold"},{"text":" XP","color":"gold"}]]}
function mgs:v5.1.0/progression/mp/award_challenge
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1

data modify storage mgs:signals on_challenge_unlock set value {branch:"mp",chain:"level",tier:7,side:"mp",xp:250}
function #mgs:progression/on_challenge_unlock
scoreboard players operation #xp_gain mgs.data = #adv_gain_prev mgs.data

