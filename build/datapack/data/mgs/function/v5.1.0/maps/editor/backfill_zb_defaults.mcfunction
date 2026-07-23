
#> mgs:v5.1.0/maps/editor/backfill_zb_defaults
#
# @executed	as @n[tag=mgs.new_zb_marker]
#
# @within	mgs:v5.1.0/maps/editor/summon_zb_object_iter [ as @n[tag=mgs.new_zb_marker] ]
#

execute if entity @s[tag=mgs.element.zombie_spawn] unless data entity @s data.activation_box run data modify entity @s data.activation_box set value []
execute if entity @s[tag=mgs.element.special_spawn] unless data entity @s data.activation_box run data modify entity @s data.activation_box set value []
execute if entity @s[tag=mgs.element.wallbuy] unless data entity @s data.name run data modify entity @s data.name set value ""
execute if entity @s[tag=mgs.element.wallbuy] unless data entity @s data.price run data modify entity @s data.price set value 1000
execute if entity @s[tag=mgs.element.wallbuy] unless data entity @s data.refill_price run data modify entity @s data.refill_price set value 500
execute if entity @s[tag=mgs.element.wallbuy] unless data entity @s data.refill_price_pap run data modify entity @s data.refill_price_pap set value 4500
execute if entity @s[tag=mgs.element.wallbuy] unless data entity @s data.weapon_id run data modify entity @s data.weapon_id set value "m1911"
execute if entity @s[tag=mgs.element.wallbuy] unless data entity @s data.magazine_id run data modify entity @s data.magazine_id set value "m1911_mag"
execute if entity @s[tag=mgs.element.door] unless data entity @s data.name run data modify entity @s data.name set value "Door"
execute if entity @s[tag=mgs.element.door] unless data entity @s data.back_name run data modify entity @s data.back_name set value "Door"
execute if entity @s[tag=mgs.element.door] unless data entity @s data.price run data modify entity @s data.price set value 1000
execute if entity @s[tag=mgs.element.door] unless data entity @s data.partial_price run data modify entity @s data.partial_price set value 0
execute if entity @s[tag=mgs.element.door] unless data entity @s data.link_id run data modify entity @s data.link_id set value 1
execute if entity @s[tag=mgs.element.door] unless data entity @s data.back_group_id run data modify entity @s data.back_group_id set value -1
execute if entity @s[tag=mgs.element.door] unless data entity @s data.block run data modify entity @s data.block set value ""
execute if entity @s[tag=mgs.element.door] unless data entity @s data.animation run data modify entity @s data.animation set value 0
execute if entity @s[tag=mgs.element.door] unless data entity @s data.sound run data modify entity @s data.sound set value ""
execute if entity @s[tag=mgs.element.trap] unless data entity @s data.price run data modify entity @s data.price set value 1000
execute if entity @s[tag=mgs.element.trap] unless data entity @s data.type run data modify entity @s data.type set value 0
execute if entity @s[tag=mgs.element.trap] unless data entity @s data.duration run data modify entity @s data.duration set value 200
execute if entity @s[tag=mgs.element.trap] unless data entity @s data.cooldown run data modify entity @s data.cooldown set value 1200
execute if entity @s[tag=mgs.element.trap] unless data entity @s data.effect_radius run data modify entity @s data.effect_radius set value [3.0f,2.0f,3.0f]
execute if entity @s[tag=mgs.element.trap] unless data entity @s data.offset_pos run data modify entity @s data.offset_pos set value [0,0,0]
execute if entity @s[tag=mgs.element.trap] unless data entity @s data.power run data modify entity @s data.power set value 1b
execute if entity @s[tag=mgs.element.perk_machine] unless data entity @s data.name run data modify entity @s data.name set value ""
execute if entity @s[tag=mgs.element.perk_machine] unless data entity @s data.price run data modify entity @s data.price set value -1
execute if entity @s[tag=mgs.element.perk_machine] unless data entity @s data.partial_price run data modify entity @s data.partial_price set value 0
execute if entity @s[tag=mgs.element.perk_machine] unless data entity @s data.perk_id run data modify entity @s data.perk_id set value "juggernog"
execute if entity @s[tag=mgs.element.perk_machine] unless data entity @s data.power run data modify entity @s data.power set value 1b
execute if entity @s[tag=mgs.element.perk_machine] unless data entity @s data.display_item run data modify entity @s data.display_item set value ""
execute if entity @s[tag=mgs.element.perk_machine] unless data entity @s data.item_model run data modify entity @s data.item_model set value ""
execute if entity @s[tag=mgs.element.wunderfizz] unless data entity @s data.name run data modify entity @s data.name set value "Der Wunderfizz"
execute if entity @s[tag=mgs.element.wunderfizz] unless data entity @s data.price run data modify entity @s data.price set value 1500
execute if entity @s[tag=mgs.element.wunderfizz] unless data entity @s data.power run data modify entity @s data.power set value 1b
execute if entity @s[tag=mgs.element.wunderfizz] unless data entity @s data.all_perks run data modify entity @s data.all_perks set value 0b
execute if entity @s[tag=mgs.element.wunderfizz] unless data entity @s data.can_start_on run data modify entity @s data.can_start_on set value 1b
execute if entity @s[tag=mgs.element.wunderfizz] unless data entity @s data.display_item run data modify entity @s data.display_item set value ""
execute if entity @s[tag=mgs.element.wunderfizz] unless data entity @s data.item_model run data modify entity @s data.item_model set value ""
execute if entity @s[tag=mgs.element.pap_machine] unless data entity @s data.name run data modify entity @s data.name set value "Pack-a-Punch"
execute if entity @s[tag=mgs.element.pap_machine] unless data entity @s data.price run data modify entity @s data.price set value 5000
execute if entity @s[tag=mgs.element.pap_machine] unless data entity @s data.power run data modify entity @s data.power set value 1b
execute if entity @s[tag=mgs.element.pap_machine] unless data entity @s data.display_item run data modify entity @s data.display_item set value ""
execute if entity @s[tag=mgs.element.pap_machine] unless data entity @s data.item_model run data modify entity @s data.item_model set value ""
execute if entity @s[tag=mgs.element.mystery_box_pos] unless data entity @s data.can_start_on run data modify entity @s data.can_start_on set value 1b
execute if entity @s[tag=mgs.element.mystery_box_pos] unless data entity @s data.display_item run data modify entity @s data.display_item set value ""
execute if entity @s[tag=mgs.element.mystery_box_pos] unless data entity @s data.item_model run data modify entity @s data.item_model set value ""
execute if entity @s[tag=mgs.element.barrier] unless data entity @s data.block_enabled run data modify entity @s data.block_enabled set value {Name:"minecraft:oak_fence_gate",Properties:{open:"false"}}
execute if entity @s[tag=mgs.element.barrier] unless data entity @s data.block_disabled run data modify entity @s data.block_disabled set value {Name:"minecraft:oak_fence_gate",Properties:{open:"true"}}
execute if entity @s[tag=mgs.element.barrier] unless data entity @s data.radius run data modify entity @s data.radius set value 2

