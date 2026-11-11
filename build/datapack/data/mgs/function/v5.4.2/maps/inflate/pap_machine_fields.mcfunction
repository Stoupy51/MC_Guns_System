
#> mgs:v5.4.2/maps/inflate/pap_machine_fields
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/inflate/pap_machine
#

function mgs:v5.4.2/maps/inflate/rotation
execute unless data storage mgs:temp _inf.name run data modify storage mgs:temp _inf.name set value "Pack-a-Punch"
execute unless data storage mgs:temp _inf.price run data modify storage mgs:temp _inf.price set value 5000
execute unless data storage mgs:temp _inf.power run data modify storage mgs:temp _inf.power set value 1b
execute unless data storage mgs:temp _inf.display_item run data modify storage mgs:temp _inf.display_item set value ""
execute unless data storage mgs:temp _inf.item_model run data modify storage mgs:temp _inf.item_model set value ""

