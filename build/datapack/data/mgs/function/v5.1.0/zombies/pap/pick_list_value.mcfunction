
#> mgs:v5.1.0/zombies/pap/pick_list_value
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.1.0/zombies/pap/apply_field
#			mgs:v5.1.0/zombies/pap/resolve_runtime_name
#

scoreboard players set #pap_pick_i mgs.data 0
data modify storage mgs:temp _pap_pick.value set from storage mgs:temp _pap_pick.list[0]
function mgs:v5.1.0/zombies/pap/pick_list_value_step

