
#> mgs:v5.3.0/maps/inflate/mystery_box_pos_fields
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/maps/inflate/mystery_box_pos
#

function mgs:v5.3.0/maps/inflate/rotation
execute unless data storage mgs:temp _inf.can_start_on run data modify storage mgs:temp _inf.can_start_on set value 1b
execute unless data storage mgs:temp _inf.display_item run data modify storage mgs:temp _inf.display_item set value ""
execute unless data storage mgs:temp _inf.item_model run data modify storage mgs:temp _inf.item_model set value ""
execute unless data storage mgs:temp _inf.location_name run data modify storage mgs:temp _inf.location_name set value ""
execute unless data storage mgs:temp _inf.pitch run data modify storage mgs:temp _inf.pitch set value 0.0f
execute unless data storage mgs:temp _inf.roll run data modify storage mgs:temp _inf.roll set value 0

