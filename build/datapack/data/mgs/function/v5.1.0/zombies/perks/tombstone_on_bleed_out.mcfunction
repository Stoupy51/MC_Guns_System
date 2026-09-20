
#> mgs:v5.1.0/zombies/perks/tombstone_on_bleed_out
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/bleed_out
#

execute unless entity @e[tag=mgs.tombstone,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run return 0
execute store result storage mgs:temp _ts_id.id int 1 run scoreboard players get @s mgs.zb.downed_id
function mgs:v5.1.0/zombies/perks/tombstone_snapshot_inv with storage mgs:temp _ts_id

