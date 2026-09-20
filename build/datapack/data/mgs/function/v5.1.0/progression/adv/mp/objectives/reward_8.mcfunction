
#> mgs:v5.1.0/progression/adv/mp/objectives/reward_8
#
# @executed	as the player & at current position
#
# @within	advancement mgs:challenges/mp/objectives_8
#

# Objective Machine: 230 XP into the mp pool
scoreboard players operation #adv_gain_prev mgs.data = #xp_gain mgs.data
scoreboard players set #xp_gain mgs.data 230
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"🏆 ","color":"white"},{"translate":"mgs.challenge_unlocked","color":"gray"},{"translate":"mgs.objective_machine","color":"yellow"},[" ",{"text":"+","color":"gold"},{"score":{"name":"#xp_gain","objective":"mgs.data"},"color":"gold"},{"text":" XP","color":"gold"}]]
function mgs:v5.1.0/progression/mp/award_challenge
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1

data modify storage mgs:signals on_challenge_unlock set value {branch:"mp",chain:"objectives",tier:8,side:"mp",xp:230}
function #mgs:progression/on_challenge_unlock
scoreboard players operation #xp_gain mgs.data = #adv_gain_prev mgs.data

