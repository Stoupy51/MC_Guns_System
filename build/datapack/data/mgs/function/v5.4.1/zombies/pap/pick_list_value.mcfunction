
#> mgs:v5.4.1/zombies/pap/pick_list_value
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/pap/apply_field
#			mgs:v5.4.1/zombies/pap/resolve_runtime_name
#

scoreboard players set #pap_pick_i mgs.data 0
data modify storage mgs:temp _pap_pick.value set from storage mgs:temp _pap_pick.list[0]
function mgs:v5.4.1/zombies/pap/pick_list_value_step

