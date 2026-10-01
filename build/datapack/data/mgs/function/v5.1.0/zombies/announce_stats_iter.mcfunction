
#> mgs:v5.1.0/zombies/announce_stats_iter
#
# @within	mgs:v5.1.0/zombies/announce_stats_iter
#			mgs:v5.1.0/zombies/game_over
#

execute unless entity @a[tag=mgs.stat_cand] run return 0

# These objectives never go negative, so 0 is a safe floor.
scoreboard players set #stat_max mgs.data 0
scoreboard players operation #stat_max mgs.data > @a[tag=mgs.stat_cand] mgs.zb.kills

# One player with that score; #stat_found keeps ties from printing at once.
scoreboard players set #stat_found mgs.data 0
execute as @a[tag=mgs.stat_cand] if score @s mgs.zb.kills = #stat_max mgs.data if score #stat_found mgs.data matches 0 run function mgs:v5.1.0/zombies/announce_stats_one

# A candidate with no score matches nothing and would recurse forever, so stragglers are dropped.
execute if score #stat_found mgs.data matches 0 run return run tag @a remove mgs.stat_cand

# Depth is bounded by the player count.
function mgs:v5.1.0/zombies/announce_stats_iter

