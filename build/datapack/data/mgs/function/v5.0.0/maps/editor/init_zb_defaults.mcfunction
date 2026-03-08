
#> mgs:v5.0.0/maps/editor/init_zb_defaults
#
# @within	mgs:v5.0.0/maps/editor/enter
#

data modify storage mgs:temp map_edit.zb_defaults.zombie_spawn set value {group_id:0}
data modify storage mgs:temp map_edit.zb_defaults.player_spawn_zb set value {group_id:0}
data modify storage mgs:temp map_edit.zb_defaults.wallbuy set value {group_id:0,price:1000,refill_price:500,refill_price_pap:2500,weapon_id:'m1911'}
data modify storage mgs:temp map_edit.zb_defaults.door set value {group_id:0,link_id:0,back_group_id:-1,block:'',animation:0,sound:''}
data modify storage mgs:temp map_edit.zb_defaults.trap set value {group_id:0,price:1000,type:0,duration:200,cooldown:600,effect_radius:[3.0f,2.0f,3.0f],power:1b}
data modify storage mgs:temp map_edit.zb_defaults.perk_machine set value {group_id:0,price:2500,perk_id:1,power:1b}
data modify storage mgs:temp map_edit.zb_defaults.mystery_box_pos set value {group_id:0,can_start_on:1b}

