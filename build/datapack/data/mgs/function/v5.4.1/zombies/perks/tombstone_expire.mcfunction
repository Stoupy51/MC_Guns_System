
#> mgs:v5.4.1/zombies/perks/tombstone_expire
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/perks/tombstone_marker_tick
#

execute store result storage mgs:temp _ts_id.id int 1 run scoreboard players get @s mgs.zb.downed_id
function mgs:v5.4.1/zombies/perks/tombstone_clear_inv with storage mgs:temp _ts_id
kill @s

