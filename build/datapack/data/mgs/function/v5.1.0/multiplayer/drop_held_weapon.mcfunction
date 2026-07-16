
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

# Never drop grenades
execute if data storage mgs:temp _dropw.components."minecraft:custom_data".mgs.stats.grenade_type run return 0

# Sync live ammo into the drop (the item's custom data only refreshes a few seconds after shooting stops);
# empty guns drop with 50% of their magazine capacity instead
scoreboard players operation #drop_ammo mgs.data = @s mgs.remaining_bullets
execute store result score #drop_half mgs.data run data get storage mgs:temp _dropw.components."minecraft:custom_data".mgs.stats.capacity
scoreboard players operation #drop_half mgs.data /= #2 mgs.data
execute if score #drop_ammo mgs.data matches ..0 run scoreboard players operation #drop_ammo mgs.data = #drop_half mgs.data
execute store result storage mgs:temp _dropw.components."minecraft:custom_data".mgs.stats.remaining_bullets int 1 run scoreboard players get #drop_ammo mgs.data

# Static item display lying flat on the ground (left_rotation = 90° around X), oriented by the dying player's yaw
summon minecraft:item_display ~ ~0.05 ~ {Tags:["mgs.mp_dropped_gun","mgs.gm_entity","mgs.mp_drop_new"],item_display:"ground",transformation:{left_rotation:[0.7071068f,0f,0f,0.7071068f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.75f,0.75f,0.75f]}}
data modify entity @n[tag=mgs.mp_drop_new] item set from storage mgs:temp _dropw
data modify entity @n[tag=mgs.mp_drop_new] Rotation[0] set from entity @s Rotation[0]
scoreboard players set @n[tag=mgs.mp_drop_new] mgs.mp.drop_timer 600
tag @n[tag=mgs.mp_drop_new] remove mgs.mp_drop_new

# Small interaction hitbox for pickup (Bookshelf right-click)
summon minecraft:interaction ~ ~ ~ {width:0.9f,height:0.6f,response:true,Tags:["mgs.mp_drop_int","mgs.gm_entity","bs.entity.interaction","mgs.mp_drop_new"]}
scoreboard players set @n[tag=mgs.mp_drop_new] mgs.mp.drop_timer 600
execute as @n[tag=mgs.mp_drop_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.1.0/multiplayer/pickup_dropped_weapon",executor:"source"}
tag @n[tag=mgs.mp_drop_new] remove mgs.mp_drop_new

