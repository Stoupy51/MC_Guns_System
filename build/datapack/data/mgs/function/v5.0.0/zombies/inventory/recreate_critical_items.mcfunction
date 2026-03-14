
#> mgs:v5.0.0/zombies/inventory/recreate_critical_items
#
# @within	???
#

execute unless items entity @s hotbar.0 *[custom_data~{mgs:{knife:true,zombies:{hotbar:0}}}] run item replace entity @s hotbar.0 with minecraft:iron_sword[unbreakable={},custom_data={mgs:{knife:true}},item_name={"translate":"mgs.knife","color":"white","italic":false},attribute_modifiers=[{type:"attack_damage",amount:20,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_damage"}]]
execute unless items entity @s hotbar.0 *[custom_data~{mgs:{knife:true,zombies:{hotbar:0}}}] run function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.0",group:"hotbar",index:0}

execute unless items entity @s hotbar.7 *[custom_data~{mgs:{gun:true,zombies:{hotbar:7}}}] run loot replace entity @s hotbar.7 loot mgs:i/frag_grenade
execute unless items entity @s hotbar.7 *[custom_data~{mgs:{gun:true,zombies:{hotbar:7}}}] run function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}
execute unless items entity @s hotbar.7 *[custom_data~{mgs:{gun:true,zombies:{hotbar:7}}}] run data modify storage mgs:temp zb_item_stats set value {capacity:4,remaining_bullets:0}
execute unless items entity @s hotbar.7 *[custom_data~{mgs:{gun:true,zombies:{hotbar:7}}}] run item modify entity @s hotbar.7 mgs:v5.0.0/zb_item_stats

execute unless items entity @s hotbar.8 *[custom_data~{mgs:{zb_info:true,zombies:{hotbar:8}}}] run function mgs:v5.0.0/zombies/inventory/refresh_info_item

