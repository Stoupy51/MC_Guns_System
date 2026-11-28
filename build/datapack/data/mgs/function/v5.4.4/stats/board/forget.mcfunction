
#> mgs:v5.4.4/stats/board/forget
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/stats/admin/reset_name {uuid:$(uuid)}
#
# @args		uuid (unknown)
#

$data remove storage mgs:stats leaderboards.level_mp[{uuid:$(uuid)}]
$data remove storage mgs:stats leaderboards.level_zb[{uuid:$(uuid)}]
data modify storage mgs:temp _fg set value {}
$data modify storage mgs:temp _fg.uuid set value $(uuid)
data modify storage mgs:temp _fg.maps set from storage mgs:maps zombies
function mgs:v5.4.4/stats/board/forget_zb_next
data modify storage mgs:temp _fg.maps set from storage mgs:maps missions
function mgs:v5.4.4/stats/board/forget_mi_next
function mgs:v5.4.4/stats/board/refresh_holograms

