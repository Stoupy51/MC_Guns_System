
#> mgs:v5.1.0/zombies/announce_stats_iter
#
# @within	mgs:v5.1.0/zombies/announce_stats_iter
#			mgs:v5.1.0/zombies/game_over
#

# Stop once every player has been announced
execute unless entity @a[tag=mgs.stat_cand] run return 0

# Highest score still unannounced (these objectives never go negative, so 0 is a safe floor)
scoreboard players set #stat_max mgs.data 0
scoreboard players operation #stat_max mgs.data > @a[tag=mgs.stat_cand] mgs.zb.kills

# Announce exactly one player holding that score; #stat_found keeps ties from all printing at once
scoreboard players set #stat_found mgs.data 0
execute as @a[tag=mgs.stat_cand] if score @s mgs.zb.kills = #stat_max mgs.data if score #stat_found mgs.data matches 0 run function mgs:v5.1.0/zombies/announce_stats_one

# Termination guarantee: a candidate with no score at all matches nothing, so no tag would be
# removed and this function would recurse until the server died. Drop the stragglers and stop.
execute if score #stat_found mgs.data matches 0 run return run tag @a remove mgs.stat_cand

# Recurse for the next player down. Depth is bounded by the player count.
function mgs:v5.1.0/zombies/announce_stats_iter

