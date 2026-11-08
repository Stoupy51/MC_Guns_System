
#> mgs:v5.4.1/stats/admin/reset
#
# @within	mgs:v5.4.1/dialog/close_then
#			string in mgs:v5.4.1/stats/menu/players_button_reset {i:$(i)}
#
# @args		i (unknown)
#

data modify storage mgs:temp _st_one set value {}
$data modify storage mgs:temp _st_one.uuid set from storage mgs:stats known[$(i)]
function mgs:v5.4.1/stats/admin/reset_uuid with storage mgs:temp _st_one

