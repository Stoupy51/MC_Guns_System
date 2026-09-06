
#> mgs:v5.1.0/progression/adv/zb/headshots/reward_10
#
# @executed	as the player & at current position
#
# @within	advancement mgs:challenges/zb/headshots_10
#

# Ten Thousand Skulls: 340 XP into the zb pool
scoreboard players operation #adv_gain_prev mgs.data = #xp_gain mgs.data
scoreboard players set #xp_gain mgs.data 340
tag @a remove mgs.xp_earner
tag @s add mgs.xp_earner
tellraw @a[tag=!mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"yellow"}],[{"text":" ","color":"gray"}, {"translate":"mgs.unlocked"}],{"translate":"mgs.ten_thousand_skulls","color":"yellow"},{"text":"!","color":"gray"}]
tellraw @a[tag=mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"yellow"}],[{"text":" ","color":"gray"}, {"translate":"mgs.unlocked"}],{"translate":"mgs.ten_thousand_skulls","color":"yellow"},{"text":"!","color":"gray"},[" ",{"text":"+","color":"gold"},{"score":{"name":"#xp_gain","objective":"mgs.data"},"color":"gold"},{"text":" XP","color":"gold"}]]
execute as @a[tag=mgs.xp_earner] run function mgs:v5.1.0/progression/zb/award_challenge
tag @a remove mgs.xp_earner
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1

data modify storage mgs:signals on_challenge_unlock set value {branch:"zb",chain:"headshots",tier:10,side:"zb",xp:340}
function #mgs:progression/on_challenge_unlock
scoreboard players operation #xp_gain mgs.data = #adv_gain_prev mgs.data

## sourceMappingURL=reward_10.mcfunction.map
