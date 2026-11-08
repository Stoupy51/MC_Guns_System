
#> mgs:v5.4.1/stats/menu/fetch
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/stats/menu/view with storage mgs:temp _sv
#
# @args		i (unknown)
#

$execute as @a[scores={mgs.st.index=$(i)}] run function mgs:v5.4.1/stats/menu/refresh_self
$data modify storage mgs:temp _sv.uuid set from storage mgs:stats known[$(i)]
function mgs:v5.4.1/stats/menu/fetch_entry with storage mgs:temp _sv

