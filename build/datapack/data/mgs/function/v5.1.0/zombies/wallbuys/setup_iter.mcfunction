
#> mgs:v5.1.0/zombies/wallbuys/setup_iter
#
# @within	mgs:v5.1.0/zombies/wallbuys/setup
#			mgs:v5.1.0/zombies/wallbuys/setup_iter
#

scoreboard players add #wb_counter mgs.data 1

execute store result score #wbx mgs.data run data get storage mgs:temp _wb_iter[0].pos[0]
execute store result score #wby mgs.data run data get storage mgs:temp _wb_iter[0].pos[1]
execute store result score #wbz mgs.data run data get storage mgs:temp _wb_iter[0].pos[2]
scoreboard players operation #wbx mgs.data += #gm_base_x mgs.data
scoreboard players operation #wby mgs.data += #gm_base_y mgs.data
scoreboard players operation #wbz mgs.data += #gm_base_z mgs.data

execute store result storage mgs:temp _wb.x int 1 run scoreboard players get #wbx mgs.data
execute store result storage mgs:temp _wb.y int 1 run scoreboard players get #wby mgs.data
execute store result storage mgs:temp _wb.z int 1 run scoreboard players get #wbz mgs.data
data modify storage mgs:temp _wb.weapon_id set from storage mgs:temp _wb_iter[0].weapon_id

# Name defaults to the weapon_id.
data modify storage mgs:temp _wb.name set from storage mgs:temp _wb_iter[0].weapon_id
execute if data storage mgs:temp _wb_iter[0].name run data modify storage mgs:temp _wb.name set from storage mgs:temp _wb_iter[0].name

data modify storage mgs:temp _wb.rotation set from storage mgs:temp _wb_iter[0].rotation

function mgs:v5.1.0/zombies/wallbuys/place_at with storage mgs:temp _wb
execute as @n[tag=mgs.wb_new] at @s run tp @s ^ ^ ^-0.5
execute as @n[tag=mgs.wb_new_display] at @s run tp @s ^ ^0.5 ^-0.49

scoreboard players operation @n[tag=mgs.wb_new] mgs.zb.wb.id = #wb_counter mgs.data
execute store result score @n[tag=mgs.wb_new] mgs.zb.wb.price run data get storage mgs:temp _wb_iter[0].price
execute store result score @n[tag=mgs.wb_new] mgs.zb.wb.rfprice run data get storage mgs:temp _wb_iter[0].refill_price
execute store result score @n[tag=mgs.wb_new] mgs.zb.wb.rfpap run data get storage mgs:temp _wb_iter[0].refill_price_pap

# magazine_id is optional on non-gun wallbuys, so it is cleared first.
execute store result storage mgs:temp _wb_store.id int 1 run scoreboard players get #wb_counter mgs.data
data modify storage mgs:temp _wb_store.weapon_id set from storage mgs:temp _wb_iter[0].weapon_id
data modify storage mgs:temp _wb_store.magazine_id set value ""
data modify storage mgs:temp _wb_store.magazine_id set from storage mgs:temp _wb_iter[0].magazine_id
data modify storage mgs:temp _wb_store.name set from storage mgs:temp _wb.name

execute as @n[tag=mgs.wb_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.1.0/zombies/wallbuys/on_right_click",executor:"source"}
execute as @n[tag=mgs.wb_new] run function #bs.interaction:on_hover {run:"function mgs:v5.1.0/zombies/wallbuys/on_hover",executor:"source"}
tag @n[tag=mgs.wb_new] remove mgs.wb_new

function mgs:v5.1.0/zombies/wallbuys/set_display_item with storage mgs:temp _wb

# For the hover title.
data modify storage mgs:temp _wb_store.item_name set from entity @n[tag=mgs.wb_new_display] item.components."minecraft:item_name"

# Kind from the item's custom_data (0 gun, 1 knife, 2 lethal, 3 tactical); tactical is tested last
# because monkey bombs carry both flags.
scoreboard players set #wb_kind mgs.data 0
execute if data entity @n[tag=mgs.wb_new_display] item.components."minecraft:custom_data".mgs.stats.grenade_type run scoreboard players set #wb_kind mgs.data 2
execute if data entity @n[tag=mgs.wb_new_display] item.components."minecraft:custom_data".mgs.tactical run scoreboard players set #wb_kind mgs.data 3
execute if data entity @n[tag=mgs.wb_new_display] item.components."minecraft:custom_data".mgs.knife run scoreboard players set #wb_kind mgs.data 1
execute store result storage mgs:temp _wb_store.kind int 1 run scoreboard players get #wb_kind mgs.data
function mgs:v5.1.0/zombies/wallbuys/store_data with storage mgs:temp _wb_store

tag @e[tag=mgs.wb_new_display] remove mgs.wb_new_display

data remove storage mgs:temp _wb_iter[0]
execute if data storage mgs:temp _wb_iter[0] run function mgs:v5.1.0/zombies/wallbuys/setup_iter

