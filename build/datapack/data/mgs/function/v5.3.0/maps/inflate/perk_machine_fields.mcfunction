
#> mgs:v5.3.0/maps/inflate/perk_machine_fields
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/inflate/perk_machine
#

function mgs:v5.3.0/maps/inflate/rotation
execute unless data storage mgs:temp _inf.name run data modify storage mgs:temp _inf.name set value ""
execute unless data storage mgs:temp _inf.price run data modify storage mgs:temp _inf.price set value -1
execute unless data storage mgs:temp _inf.partial_price run data modify storage mgs:temp _inf.partial_price set value 0
execute unless data storage mgs:temp _inf.perk_id run data modify storage mgs:temp _inf.perk_id set value "juggernog"
execute unless data storage mgs:temp _inf.power run data modify storage mgs:temp _inf.power set value 1b
execute unless data storage mgs:temp _inf.display_item run data modify storage mgs:temp _inf.display_item set value ""
execute unless data storage mgs:temp _inf.item_model run data modify storage mgs:temp _inf.item_model set value ""

