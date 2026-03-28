
#> mgs:v5.0.0/zombies/pap/resolve_runtime_name
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click
#

data modify storage mgs:temp _pap_pick.list set from storage mgs:temp _pap_extract.stats.pap_stats.pap_name
execute if data storage mgs:temp _pap_pick.list[0] run function mgs:v5.0.0/zombies/pap/pick_list_value
execute if data storage mgs:temp _pap_pick.list[0] run data modify storage mgs:temp _pap_extract.new_name set from storage mgs:temp _pap_pick.value
execute unless data storage mgs:temp _pap_pick.list[0] run data modify storage mgs:temp _pap_extract.new_name set from storage mgs:temp _pap_extract.stats.pap_stats.pap_name

