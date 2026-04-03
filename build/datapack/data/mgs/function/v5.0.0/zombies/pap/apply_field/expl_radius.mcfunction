
#> mgs:v5.0.0/zombies/pap/apply_field/expl_radius
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/apply_runtime_overrides
#

data modify storage mgs:temp _pap_pick.list set from storage mgs:temp _pap_extract.stats.pap_stats.expl_radius
execute if data storage mgs:temp _pap_pick.list[0] run function mgs:v5.0.0/zombies/pap/pick_list_value
execute if data storage mgs:temp _pap_pick.list[0] run data modify storage mgs:temp _pap_extract.stats.expl_radius set from storage mgs:temp _pap_pick.value
execute unless data storage mgs:temp _pap_pick.list[0] run data modify storage mgs:temp _pap_extract.stats.expl_radius set from storage mgs:temp _pap_extract.stats.pap_stats.expl_radius

