
#> mgs:v5.1.0/progression/adv/zb/kills/reward_3
#
# @executed	as the player & at current position
#
# @within	advancement mgs:challenges/zb/kills_3
#

# Culling: 30 XP into the zb pool
scoreboard players operation #adv_gain_prev mgs.data = #xp_gain mgs.data
scoreboard players set #xp_gain mgs.data 30
tag @s add mgs.xp_earner
tellraw @a[tag=!mgs.xp_earner] {"text":"","hover_event":{"action":"show_text","value":[{"translate":"mgs.culling","color":"yellow"},"\n",{"translate":"mgs.kill_500_zombies","color":"gray"}]},"extra":[[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"🏆 ","color":"white"},["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"yellow"}],[{"text":" ","color":"gray"}, {"translate":"mgs.unlocked_challenge"}],{"translate":"mgs.culling","color":"yellow"}]}
tag @s remove mgs.xp_earner
tellraw @s {"text":"","hover_event":{"action":"show_text","value":[{"translate":"mgs.culling","color":"yellow"},"\n",{"translate":"mgs.kill_500_zombies","color":"gray"}]},"extra":[[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"🏆 ","color":"white"},{"translate":"mgs.challenge_unlocked","color":"gray"},{"translate":"mgs.culling","color":"yellow"},[" ",{"text":"+","color":"gold"},{"score":{"name":"#xp_gain","objective":"mgs.data"},"color":"gold"},{"text":" XP","color":"gold"}]]}
function mgs:v5.1.0/progression/zb/award_challenge
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1

data modify storage mgs:signals on_challenge_unlock set value {branch:"zb",chain:"kills",tier:3,side:"zb",xp:30}
function #mgs:progression/on_challenge_unlock
scoreboard players operation #xp_gain mgs.data = #adv_gain_prev mgs.data

