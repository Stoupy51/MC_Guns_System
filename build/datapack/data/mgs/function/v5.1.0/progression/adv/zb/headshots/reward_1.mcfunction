
#> mgs:v5.1.0/progression/adv/zb/headshots/reward_1
#
# @executed	as the player & at current position
#
# @within	advancement mgs:challenges/zb/headshots_1
#

# Aim For The Head: 10 XP into the zb pool
scoreboard players operation #adv_gain_prev mgs.data = #xp_gain mgs.data
scoreboard players set #xp_gain mgs.data 10
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"🏆 ","color":"white"},{"translate":"mgs.challenge_unlocked","color":"gray"},{"translate":"mgs.aim_for_the_head","color":"yellow"},[" ",{"text":"+","color":"gold"},{"score":{"name":"#xp_gain","objective":"mgs.data"},"color":"gold"},{"text":" XP","color":"gold"}]]
function mgs:v5.1.0/progression/zb/award_challenge
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1

data modify storage mgs:signals on_challenge_unlock set value {branch:"zb",chain:"headshots",tier:1,side:"zb",xp:10}
function #mgs:progression/on_challenge_unlock
scoreboard players operation #xp_gain mgs.data = #adv_gain_prev mgs.data

