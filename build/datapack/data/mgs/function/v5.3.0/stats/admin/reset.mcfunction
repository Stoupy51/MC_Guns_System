
#> mgs:v5.3.0/stats/admin/reset
#
# @within	string in mgs:v5.3.0/stats/menu/players_button_reset {i:$(i)}
#
# @args		i (unknown)
#

data modify storage mgs:temp _st_one set value {}
$data modify storage mgs:temp _st_one.uuid set from storage mgs:stats known[$(i)]
function mgs:v5.3.0/stats/admin/reset_uuid with storage mgs:temp _st_one

