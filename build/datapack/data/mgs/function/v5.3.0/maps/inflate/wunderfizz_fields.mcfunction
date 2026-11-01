
#> mgs:v5.3.0/maps/inflate/wunderfizz_fields
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/maps/inflate/wunderfizz
#

function mgs:v5.3.0/maps/inflate/rotation
execute unless data storage mgs:temp _inf.name run data modify storage mgs:temp _inf.name set value "Der Wunderfizz"
execute unless data storage mgs:temp _inf.price run data modify storage mgs:temp _inf.price set value 1500
execute unless data storage mgs:temp _inf.power run data modify storage mgs:temp _inf.power set value 1b
execute unless data storage mgs:temp _inf.all_perks run data modify storage mgs:temp _inf.all_perks set value 0b
execute unless data storage mgs:temp _inf.can_start_on run data modify storage mgs:temp _inf.can_start_on set value 1b
execute unless data storage mgs:temp _inf.display_item run data modify storage mgs:temp _inf.display_item set value ""
execute unless data storage mgs:temp _inf.item_model run data modify storage mgs:temp _inf.item_model set value ""

