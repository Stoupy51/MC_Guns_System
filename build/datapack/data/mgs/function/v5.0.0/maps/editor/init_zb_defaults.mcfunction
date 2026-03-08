
#> mgs:v5.0.0/maps/editor/init_zb_defaults
#
# @within	mgs:v5.0.0/maps/editor/enter
#

data modify storage mgs:temp map_edit.zb_defaults.group_id set value 0
data modify storage mgs:temp map_edit.zb_defaults.zombie_spawn set value {}
data modify storage mgs:temp map_edit.zb_defaults.player_spawn_zb set value {}
data modify storage mgs:temp map_edit.zb_defaults.wallbuy set value {price:1000,refill_price:500,refill_price_pap:4500,weapon_id:'m1911'}
data modify storage mgs:temp map_edit.zb_defaults.door set value {price:1000,link_id:1,back_group_id:-1,block:'',animation:0,sound:''}
data modify storage mgs:temp map_edit.zb_defaults.trap set value {price:1000,type:0,duration:200,cooldown:1200,effect_radius:[3.0f,2.0f,3.0f],offset_pos:[0,0,0],power:1b}
data modify storage mgs:temp map_edit.zb_defaults.perk_machine set value {price:2500,perk_id:'juggernog',power:1b}
data modify storage mgs:temp map_edit.zb_defaults.mystery_box_pos set value {can_start_on:1b}
data modify storage mgs:temp map_edit.zb_defaults.power_switch set value {}

