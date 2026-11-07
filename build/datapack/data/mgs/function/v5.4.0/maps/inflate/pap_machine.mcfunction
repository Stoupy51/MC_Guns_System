
#> mgs:v5.4.0/maps/inflate/pap_machine
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/inflate
#			mgs:v5.4.0/maps/inflate/pap_machine
#

data modify storage mgs:temp _inf set from storage mgs:temp _inf_src[0]
function mgs:v5.4.0/maps/inflate/pap_machine_fields
data modify storage mgs:temp _inf_map.pap_machines append from storage mgs:temp _inf
data remove storage mgs:temp _inf_src[0]
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.0/maps/inflate/pap_machine

