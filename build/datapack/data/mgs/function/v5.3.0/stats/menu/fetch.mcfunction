
#> mgs:v5.3.0/stats/menu/fetch
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/view with storage mgs:temp _sv
#
# @args		i (unknown)
#

$execute as @a[scores={mgs.st.index=$(i)}] run function mgs:v5.3.0/stats/menu/refresh_self
$data modify storage mgs:temp _sv.uuid set from storage mgs:stats known[$(i)]
function mgs:v5.3.0/stats/menu/fetch_entry with storage mgs:temp _sv

