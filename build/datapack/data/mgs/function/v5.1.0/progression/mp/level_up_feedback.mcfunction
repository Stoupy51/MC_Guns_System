
#> mgs:v5.1.0/progression/mp/level_up_feedback
#
# @within	mgs:v5.1.0/progression/mp/settle
#

data modify storage smithed.actionbar:input message set value {json:[{"text":"⬆ ","color":"white"},{"translate":"mgs.multiplayer_level","color":"gold"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"yellow"}],priority:"override",freeze:60}
function #smithed.actionbar:message
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"⬆ ","color":"white"},{"translate":"mgs.multiplayer_level_up_you_are_now_level","color":"yellow"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":".","color":"yellow"}]
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1.2

# @s = the player who levelled; #xp_lvl_before still holds the level they came from
data modify storage mgs:signals on_level_up set value {side:"mp"}
function #mgs:progression/on_level_up

