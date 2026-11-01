
#> mgs:v5.3.0/maps/compact/door
#
# @executed	as @e[tag=mgs.element.player_spawn_zb] & at @s
#
# @within	mgs:v5.3.0/maps/editor/save_zb_object
#

data remove storage mgs:temp _save_zb.group_id
execute if data storage mgs:temp _save_zb{name:"Door"} run data remove storage mgs:temp _save_zb.name
execute if data storage mgs:temp _save_zb{back_name:"Door"} run data remove storage mgs:temp _save_zb.back_name
execute if data storage mgs:temp _save_zb{price:1000} run data remove storage mgs:temp _save_zb.price
execute if data storage mgs:temp _save_zb{partial_price:0} run data remove storage mgs:temp _save_zb.partial_price
execute if data storage mgs:temp _save_zb{back_group_id:-1} run data remove storage mgs:temp _save_zb.back_group_id
execute if data storage mgs:temp _save_zb{min_round:0} run data remove storage mgs:temp _save_zb.min_round
execute if data storage mgs:temp _save_zb{animation:0} run data remove storage mgs:temp _save_zb.animation
execute if data storage mgs:temp _save_zb{sound:""} run data remove storage mgs:temp _save_zb.sound
function mgs:v5.3.0/maps/compact/door_block

