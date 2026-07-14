
#> mgs:v5.1.0/multiplayer/drop_held_weapon
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/enter_death_spectate [ at @s ]
#

# Only drop a gun held in the selected weapon slot (hotbar.0 or hotbar.1)
execute store result score #drop_sel mgs.data run data get entity @s SelectedItemSlot
execute unless score #drop_sel mgs.data matches 0..1 run scoreboard players set #drop_sel mgs.data 0
execute if score #drop_sel mgs.data matches 0 unless items entity @s hotbar.0 *[custom_data~{mgs:{gun:true}}] run return 0
execute if score #drop_sel mgs.data matches 1 unless items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run return 0

# Capture the held gun item (strip the inventory Slot tag so it fits an item_display / item entity)
execute if score #drop_sel mgs.data matches 0 run data modify storage mgs:temp _dropw set from entity @s Inventory[{Slot:0b}]
execute if score #drop_sel mgs.data matches 1 run data modify storage mgs:temp _dropw set from entity @s Inventory[{Slot:1b}]
data remove storage mgs:temp _dropw.Slot

# Static item display resting on the ground (no gravity, never moves)
summon minecraft:item_display ~ ~0.1 ~ {Tags:["mgs.mp_dropped_gun","mgs.gm_entity","mgs.mp_drop_new"],item_display:"ground",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.75f,0.75f,0.75f]}}
data modify entity @n[tag=mgs.mp_drop_new] item set from storage mgs:temp _dropw
scoreboard players set @n[tag=mgs.mp_drop_new] mgs.mp.drop_timer 600
tag @n[tag=mgs.mp_drop_new] remove mgs.mp_drop_new

# Small interaction hitbox for pickup (Bookshelf right-click)
summon minecraft:interaction ~ ~ ~ {width:0.9f,height:0.6f,response:true,Tags:["mgs.mp_drop_int","mgs.gm_entity","bs.entity.interaction","mgs.mp_drop_new"]}
scoreboard players set @n[tag=mgs.mp_drop_new] mgs.mp.drop_timer 600
execute as @n[tag=mgs.mp_drop_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.1.0/multiplayer/pickup_dropped_weapon",executor:"source"}
tag @n[tag=mgs.mp_drop_new] remove mgs.mp_drop_new

