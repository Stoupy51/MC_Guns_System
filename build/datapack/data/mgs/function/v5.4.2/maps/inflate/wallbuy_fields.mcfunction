
#> mgs:v5.4.2/maps/inflate/wallbuy_fields
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/inflate/wallbuy
#

function mgs:v5.4.2/maps/inflate/rotation
execute unless data storage mgs:temp _inf.name run data modify storage mgs:temp _inf.name set value ""
execute unless data storage mgs:temp _inf.price run data modify storage mgs:temp _inf.price set value 1000
execute unless data storage mgs:temp _inf.refill_price run data modify storage mgs:temp _inf.refill_price set value 500
execute unless data storage mgs:temp _inf.refill_price_pap run data modify storage mgs:temp _inf.refill_price_pap set value 4500
execute unless data storage mgs:temp _inf.weapon_id run data modify storage mgs:temp _inf.weapon_id set value "m1911"
execute unless data storage mgs:temp _inf.magazine_id run data modify storage mgs:temp _inf.magazine_id set value "m1911_mag"

