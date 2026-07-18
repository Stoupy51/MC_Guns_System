
#> mgs:v5.1.0/zombies/announce_stats_one
#
# @executed	as @a[tag=mgs.stat_cand]
#
# @within	mgs:v5.1.0/zombies/announce_stats_iter [ as @a[tag=mgs.stat_cand] ]
#

# @s = the highest-scoring player not yet announced
scoreboard players set #stat_found mgs.data 1
tag @s remove mgs.stat_cand
tellraw @a ["","  ","🎖 ",{"selector":"@s"}," — Kills: ",{"score":{"name":"@s","objective":"mgs.zb.kills"},"color":"green"}," | Downs: ",{"score":{"name":"@s","objective":"mgs.zb.downs"},"color":"red"}," | Points: ",{"score":{"name":"@s","objective":"mgs.zb.points"},"color":"gold"}]

