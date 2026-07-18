
#> mgs:v5.1.0/multiplayer/announce_stats_one
#
# @executed	as @a[tag=mgs.stat_cand]
#
# @within	mgs:v5.1.0/multiplayer/announce_stats_iter [ as @a[tag=mgs.stat_cand] ]
#

# @s = the highest-scoring player not yet announced
scoreboard players set #stat_found mgs.data 1
tag @s remove mgs.stat_cand
tellraw @a ["","  ",{"selector":"@s"},{"text":" ➤ ","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.kills"},"color":"green"},[{"text":" ","color":"gray"}, {"translate":"mgs.kills"}],{"text":" · ","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.deaths"},"color":"red"},[{"text":" ","color":"gray"}, {"translate":"mgs.deaths"}]]

