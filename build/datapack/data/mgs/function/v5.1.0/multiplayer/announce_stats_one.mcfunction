
#> mgs:v5.1.0/multiplayer/announce_stats_one
#
# @executed	as @a[tag=mgs.stat_cand]
#
# @within	mgs:v5.1.0/multiplayer/announce_stats_iter [ as @a[tag=mgs.stat_cand] ]
#

# @s = the highest-scoring player not yet announced
scoreboard players set #stat_found mgs.data 1
tag @s remove mgs.stat_cand
tellraw @a ["","  ",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}],{"text":" ➤ ","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.kills"},"color":"green"},[{"text":" ","color":"gray"}, {"translate":"mgs.kills"}],{"text":" · ","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.deaths"},"color":"red"},[{"text":" ","color":"gray"}, {"translate":"mgs.deaths"}],{"text":" · ","color":"dark_gray"},{"text":"+","color":"gold"},{"score":{"name":"@s","objective":"mgs.mp.xp_session"},"color":"gold"},{"text":" XP","color":"gold"}]

