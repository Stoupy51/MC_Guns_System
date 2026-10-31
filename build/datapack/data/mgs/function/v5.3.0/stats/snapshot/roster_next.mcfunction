
#> mgs:v5.3.0/stats/snapshot/roster_next
#
# @within	mgs:v5.3.0/stats/zb/game_end {mode:"zb"}
#			mgs:v5.3.0/stats/mp/game_end {mode:"mp"}
#			mgs:v5.3.0/stats/mi/game_end {mode:"mi"}
#			mgs:v5.3.0/stats/snapshot/roster_next {mode:"$(mode)"}
#
# @args		mode (string)
#

execute unless data storage mgs:temp _st_roster[0] run return 0

data modify storage mgs:temp _st_one set value {}
data modify storage mgs:temp _st_one.uuid set from storage mgs:temp _st_roster[0]
function mgs:v5.3.0/stats/snapshot/by_uuid with storage mgs:temp _st_one
data modify storage mgs:temp _st_one.map_id set from storage mgs:temp _st_map
$function mgs:v5.3.0/stats/$(mode)/player_end with storage mgs:temp _st_one

data remove storage mgs:temp _st_roster[0]
$function mgs:v5.3.0/stats/snapshot/roster_next {mode:"$(mode)"}

