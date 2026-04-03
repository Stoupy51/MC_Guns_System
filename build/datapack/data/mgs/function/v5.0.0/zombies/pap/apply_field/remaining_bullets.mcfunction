
#> mgs:v5.0.0/zombies/pap/apply_field/remaining_bullets
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/apply_runtime_overrides
#

data modify storage mgs:temp _pap_pick.list set from storage mgs:temp _pap_extract.stats.pap_stats.remaining_bullets
execute if data storage mgs:temp _pap_pick.list[0] run function mgs:v5.0.0/zombies/pap/pick_list_value
execute if data storage mgs:temp _pap_pick.list[0] run data modify storage mgs:temp _pap_extract.stats.remaining_bullets set from storage mgs:temp _pap_pick.value
execute unless data storage mgs:temp _pap_pick.list[0] run data modify storage mgs:temp _pap_extract.stats.remaining_bullets set from storage mgs:temp _pap_extract.stats.pap_stats.remaining_bullets

