
#> mgs:v5.1.0/zombies/perks/tombstone_expire
#
# @executed	as @e[tag=mgs.tombstone,scores={mgs.zb.ts.state=1}] & at @s
#
# @within	mgs:v5.1.0/zombies/perks/tombstone_marker_tick
#

execute store result storage mgs:temp _ts_id.id int 1 run scoreboard players get @s mgs.zb.downed_id
function mgs:v5.1.0/zombies/perks/tombstone_clear_inv with storage mgs:temp _ts_id
kill @s

