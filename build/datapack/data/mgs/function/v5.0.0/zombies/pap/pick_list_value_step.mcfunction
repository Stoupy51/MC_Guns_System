
#> mgs:v5.0.0/zombies/pap/pick_list_value_step
#
# @within	mgs:v5.0.0/zombies/pap/pick_list_value
#			mgs:v5.0.0/zombies/pap/pick_list_value_advance
#

execute if score #pap_pick_i mgs.data < #pap_next_idx mgs.data if data storage mgs:temp _pap_pick.list[1] run function mgs:v5.0.0/zombies/pap/pick_list_value_advance

