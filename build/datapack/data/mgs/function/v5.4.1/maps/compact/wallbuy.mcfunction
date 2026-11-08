
#> mgs:v5.4.1/maps/compact/wallbuy
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/save_zb_object
#

data remove storage mgs:temp _save_zb.group_id
execute if data storage mgs:temp _save_zb{name:""} run data remove storage mgs:temp _save_zb.name
execute if data storage mgs:temp _save_zb{price:1000} run data remove storage mgs:temp _save_zb.price
execute if data storage mgs:temp _save_zb{refill_price:500} run data remove storage mgs:temp _save_zb.refill_price
execute if data storage mgs:temp _save_zb{refill_price_pap:4500} run data remove storage mgs:temp _save_zb.refill_price_pap
execute if data storage mgs:temp _save_zb{weapon_id:"m1911"} run data remove storage mgs:temp _save_zb.weapon_id
execute if data storage mgs:temp _save_zb{magazine_id:"m1911_mag"} run data remove storage mgs:temp _save_zb.magazine_id
data modify storage mgs:temp map_edit.map.wallbuys append from storage mgs:temp _save_zb

