
#> mgs:v5.1.0/progression/mp/level_up_feedback
#
# @within	mgs:v5.1.0/progression/mp/settle
#

data modify storage smithed.actionbar:input message set value {json:[{"text":"⬆ ","color":"gold"},{"translate":"mgs.multiplayer_level","color":"gold","bold":true},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"yellow","bold":true}],priority:"override",freeze:60}
function #smithed.actionbar:message
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"⬆ ","color":"gold"},{"translate":"mgs.multiplayer_level_up_you_are_now_level","color":"yellow"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold","bold":true},{"text":".","color":"yellow"}]
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1.2

# @s = the player who levelled; #xp_lvl_before still holds the level they came from
data modify storage mgs:signals on_level_up set value {side:"mp"}
function #mgs:progression/on_level_up

