
#> mgs:v5.1.0/progression/adv/zb/best_round/reward_10
#
# @executed	as the player & at current position
#
# @within	advancement mgs:challenges/zb/best_round_10
#

# Round 60: 505 XP into the zb pool
scoreboard players operation #adv_gain_prev mgs.data = #xp_gain mgs.data
scoreboard players set #xp_gain mgs.data 505
tag @s add mgs.xp_earner
tellraw @a[tag=!mgs.xp_earner] {"text":"","hover_event":{"action":"show_text","value":[[{"translate":"mgs.round","color":"yellow"}, " 60"],"\n",[{"translate":"mgs.clear_round","color":"gray"}, " 60"]]},"extra":[[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"🏆 ","color":"white"},["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"yellow"}],[{"text":" ","color":"gray"}, {"translate":"mgs.unlocked_challenge"}],[{"translate":"mgs.round","color":"yellow"}, " 60"]]}
tag @s remove mgs.xp_earner
tellraw @s {"text":"","hover_event":{"action":"show_text","value":[[{"translate":"mgs.round","color":"yellow"}, " 60"],"\n",[{"translate":"mgs.clear_round","color":"gray"}, " 60"]]},"extra":[[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"🏆 ","color":"white"},{"translate":"mgs.challenge_unlocked","color":"gray"},[{"translate":"mgs.round","color":"yellow"}, " 60"],[" ",{"text":"+","color":"gold"},{"score":{"name":"#xp_gain","objective":"mgs.data"},"color":"gold"},{"text":" XP","color":"gold"}]]}
function mgs:v5.1.0/progression/zb/award_challenge
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1

data modify storage mgs:signals on_challenge_unlock set value {branch:"zb",chain:"best_round",tier:10,side:"zb",xp:505}
function #mgs:progression/on_challenge_unlock
scoreboard players operation #xp_gain mgs.data = #adv_gain_prev mgs.data

