
#> mgs:v5.3.0/progression/zb/level_up_feedback
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.3.0/progression/zb/settle
#

data modify storage smithed.actionbar:input message set value {json:[{"text":"⬆ ","color":"white"},{"translate":"mgs.zombies_level","fallback":"Zombies level ","color":"gold"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"yellow"}],priority:"override",freeze:60}
function #smithed.actionbar:message
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"⬆ ","color":"white"},{"translate":"mgs.zombies_level_up_you_are_now_level","fallback":"Zombies level up! You are now level ","color":"yellow"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":".","color":"yellow"}]
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1.2

# Run as the player who levelled; #xp_lvl_before holds the previous level.
data modify storage mgs:signals on_level_up set value {side:"zb"}
function #mgs:progression/on_level_up

