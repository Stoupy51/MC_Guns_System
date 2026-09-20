
#> mgs:v5.1.0/progression/adv/zb/level/reward_7
#
# @executed	as the player & at current position
#
# @within	advancement mgs:challenges/zb/level_7
#

# Zombies Rank 100: 250 XP into the zb pool
scoreboard players operation #adv_gain_prev mgs.data = #xp_gain mgs.data
scoreboard players set #xp_gain mgs.data 250
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"🏆 ","color":"white"},{"translate":"mgs.challenge_unlocked","color":"gray"},[{"translate":"mgs.zombies_rank","color":"yellow"}, " 100"],[" ",{"text":"+","color":"gold"},{"score":{"name":"#xp_gain","objective":"mgs.data"},"color":"gold"},{"text":" XP","color":"gold"}]]
function mgs:v5.1.0/progression/zb/award_challenge
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1

data modify storage mgs:signals on_challenge_unlock set value {branch:"zb",chain:"level",tier:7,side:"zb",xp:250}
function #mgs:progression/on_challenge_unlock
scoreboard players operation #xp_gain mgs.data = #adv_gain_prev mgs.data

