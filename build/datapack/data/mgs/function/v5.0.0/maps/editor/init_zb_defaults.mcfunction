
#> mgs:v5.0.0/maps/editor/init_zb_defaults
#
# @within	mgs:v5.0.0/maps/editor/enter
#

data modify storage mgs:temp map_edit.zb_defaults.group_id set value 0
data modify storage mgs:temp map_edit.zb_defaults.zombie_spawn set value {}
data modify storage mgs:temp map_edit.zb_defaults.player_spawn_zb set value {}
data modify storage mgs:temp map_edit.zb_defaults.wallbuy set value {name:"",price:1000,refill_price:500,refill_price_pap:4500,weapon_id:"m1911",magazine_id:"m1911_mag"}
data modify storage mgs:temp map_edit.zb_defaults.door set value {name:"Door",back_name:"Door",price:1000,link_id:1,back_group_id:-1,block:"",animation:0,sound:""}
data modify storage mgs:temp map_edit.zb_defaults.trap set value {price:1000,type:0,duration:200,cooldown:1200,effect_radius:[3.0f,2.0f,3.0f],offset_pos:[0,0,0],power:1b}
data modify storage mgs:temp map_edit.zb_defaults.perk_machine set value {name:"Juggernog",price:2500,perk_id:"juggernog",power:1b,display_item:"",item_model:""}
data modify storage mgs:temp map_edit.zb_defaults.pap_machine set value {name:"Pack-a-Punch",price:5000,power:1b,display_item:"",item_model:""}
data modify storage mgs:temp map_edit.zb_defaults.mystery_box_pos set value {can_start_on:1b,display_item:"",item_model:""}
data modify storage mgs:temp map_edit.zb_defaults.power_switch set value {}
data modify storage mgs:temp map_edit.zb_defaults.barrier set value {block_enabled:{Name:"minecraft:oak_fence_gate",Properties:{open:"false"}},block_disabled:{Name:"minecraft:oak_fence_gate",Properties:{open:"true"}},radius:2}

