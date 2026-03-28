
#> mgs:v5.0.0/zombies/pap/pick_list_value_advance
#
# @within	mgs:v5.0.0/zombies/pap/pick_list_value_step
#

data remove storage mgs:temp _pap_pick.list[0]
scoreboard players add #pap_pick_i mgs.data 1
data modify storage mgs:temp _pap_pick.value set from storage mgs:temp _pap_pick.list[0]
function mgs:v5.0.0/zombies/pap/pick_list_value_step

