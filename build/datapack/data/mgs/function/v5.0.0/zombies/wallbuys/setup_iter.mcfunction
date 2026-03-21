
#> mgs:v5.0.0/zombies/wallbuys/setup_iter
#
# @within	mgs:v5.0.0/zombies/wallbuys/setup
#			mgs:v5.0.0/zombies/wallbuys/setup_iter
#

# Assign incrementing ID
scoreboard players add #wb_counter mgs.data 1

# Read relative position and convert to absolute
execute store result score #wbx mgs.data run data get storage mgs:temp _wb_iter[0].pos[0]
execute store result score #wby mgs.data run data get storage mgs:temp _wb_iter[0].pos[1]
execute store result score #wbz mgs.data run data get storage mgs:temp _wb_iter[0].pos[2]
scoreboard players operation #wbx mgs.data += #gm_base_x mgs.data
scoreboard players operation #wby mgs.data += #gm_base_y mgs.data
scoreboard players operation #wbz mgs.data += #gm_base_z mgs.data

# Store absolute position and weapon_id for macro
execute store result storage mgs:temp _wb.x int 1 run scoreboard players get #wbx mgs.data
execute store result storage mgs:temp _wb.y int 1 run scoreboard players get #wby mgs.data
execute store result storage mgs:temp _wb.z int 1 run scoreboard players get #wbz mgs.data
data modify storage mgs:temp _wb.weapon_id set from storage mgs:temp _wb_iter[0].weapon_id

# Read display name (default to weapon_id, override with "name" field)
data modify storage mgs:temp _wb.name set from storage mgs:temp _wb_iter[0].weapon_id
execute if data storage mgs:temp _wb_iter[0].name run data modify storage mgs:temp _wb.name set from storage mgs:temp _wb_iter[0].name

# Read rotation
data modify storage mgs:temp _wb.rotation set from storage mgs:temp _wb_iter[0].rotation

# Summon interaction + item display entities
function mgs:v5.0.0/zombies/wallbuys/place_at with storage mgs:temp _wb
execute as @n[tag=mgs.wb_new] at @s run tp @s ^ ^ ^0.5
execute as @n[tag=mgs.wb_new_display] at @s run tp @s ^ ^0.5 ^0.47

# Set scoreboards on interaction entity
scoreboard players operation @n[tag=mgs.wb_new] mgs.zb.wb.id = #wb_counter mgs.data
execute store result score @n[tag=mgs.wb_new] mgs.zb.wb.price run data get storage mgs:temp _wb_iter[0].price
execute store result score @n[tag=mgs.wb_new] mgs.zb.wb.rfprice run data get storage mgs:temp _wb_iter[0].refill_price
execute store result score @n[tag=mgs.wb_new] mgs.zb.wb.rfpap run data get storage mgs:temp _wb_iter[0].refill_price_pap

# Store weapon_id in indexed storage for later lookup
execute store result storage mgs:temp _wb_store.id int 1 run scoreboard players get #wb_counter mgs.data
data modify storage mgs:temp _wb_store.weapon_id set from storage mgs:temp _wb_iter[0].weapon_id
data modify storage mgs:temp _wb_store.name set from storage mgs:temp _wb.name

# Register Bookshelf events
execute as @n[tag=mgs.wb_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.0/zombies/wallbuys/on_right_click",executor:"source"}
execute as @n[tag=mgs.wb_new] run function #bs.interaction:on_hover {run:"function mgs:v5.0.0/zombies/wallbuys/on_hover",executor:"source"}
tag @n[tag=mgs.wb_new] remove mgs.wb_new

# Set item on display entity
function mgs:v5.0.0/zombies/wallbuys/set_display_item with storage mgs:temp _wb

# Capture displayed item_name for hover title
data modify storage mgs:temp _wb_store.item_name set from entity @n[tag=mgs.wb_new_display] item.components."minecraft:item_name"
function mgs:v5.0.0/zombies/wallbuys/store_data with storage mgs:temp _wb_store

tag @e[tag=mgs.wb_new_display] remove mgs.wb_new_display

# Continue iteration
data remove storage mgs:temp _wb_iter[0]
execute if data storage mgs:temp _wb_iter[0] run function mgs:v5.0.0/zombies/wallbuys/setup_iter

