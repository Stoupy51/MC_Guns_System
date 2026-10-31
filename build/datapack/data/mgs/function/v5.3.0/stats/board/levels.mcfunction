
#> mgs:v5.3.0/stats/board/levels
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/login_as with storage mgs:temp _st
#			mgs:v5.3.0/stats/mp/player_end with storage mgs:temp _st_one
#			mgs:v5.3.0/stats/zb/player_end with storage mgs:temp _st_one
#			mgs:v5.3.0/stats/mi/player_end with storage mgs:temp _st_one
#
# @args		uuid (unknown)
#			name (unknown)
#

scoreboard players set #lb_desc mgs.data 1
data modify storage mgs:temp _lb set value {path:"level_mp",entry:{}}
$data modify storage mgs:temp _lb.uuid set value $(uuid)
data modify storage mgs:temp _lb.entry.uuid set from storage mgs:temp _lb.uuid
$execute store result storage mgs:temp _lb.value int 1 store result storage mgs:temp _lb.entry.value int 1 run scoreboard players get $(name) mgs.mp.xp_total
function mgs:v5.3.0/stats/board/insert with storage mgs:temp _lb
data modify storage mgs:temp _lb set value {path:"level_zb",entry:{}}
$data modify storage mgs:temp _lb.uuid set value $(uuid)
data modify storage mgs:temp _lb.entry.uuid set from storage mgs:temp _lb.uuid
$execute store result storage mgs:temp _lb.value int 1 store result storage mgs:temp _lb.entry.value int 1 run scoreboard players get $(name) mgs.zb.xp_total
function mgs:v5.3.0/stats/board/insert with storage mgs:temp _lb

