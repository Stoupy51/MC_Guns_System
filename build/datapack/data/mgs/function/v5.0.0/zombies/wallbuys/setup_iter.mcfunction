
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

# Read facing (default 0 = south)
data modify storage mgs:temp _wb.facing set value 0
execute store result storage mgs:temp _wb.facing int 1 run data get storage mgs:temp _wb_iter[0].facing

# Summon interaction + item display entities
function mgs:v5.0.0/zombies/wallbuys/place_at with storage mgs:temp _wb

# Set scoreboards on interaction entity
scoreboard players operation @n[tag=_wb_new] mgs.zb.wb.id = #wb_counter mgs.data
execute store result score @n[tag=_wb_new] mgs.zb.wb.price run data get storage mgs:temp _wb_iter[0].price
execute store result score @n[tag=_wb_new] mgs.zb.wb.rfprice run data get storage mgs:temp _wb_iter[0].refill_price
execute store result score @n[tag=_wb_new] mgs.zb.wb.rfpap run data get storage mgs:temp _wb_iter[0].refill_price_pap

# Store weapon_id in indexed storage for later lookup
execute store result storage mgs:temp _wb_store.id int 1 run scoreboard players get #wb_counter mgs.data
data modify storage mgs:temp _wb_store.weapon_id set from storage mgs:temp _wb_iter[0].weapon_id
function mgs:v5.0.0/zombies/wallbuys/store_data with storage mgs:temp _wb_store

# Register Bookshelf events
execute as @n[tag=_wb_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.0/zombies/wallbuys/on_right_click",executor:"source"}
execute as @n[tag=_wb_new] run function #bs.interaction:on_hover_enter {run:"function mgs:v5.0.0/zombies/wallbuys/on_hover_enter",executor:"source"}
execute as @n[tag=_wb_new] run function #bs.interaction:on_hover_leave {run:"function mgs:v5.0.0/zombies/wallbuys/on_hover_leave",executor:"source"}
tag @n[tag=_wb_new] remove _wb_new

# Set item on display entity
function mgs:v5.0.0/zombies/wallbuys/set_display_item with storage mgs:temp _wb
tag @e[tag=mgs.wb_new_display] remove mgs.wb_new_display

# Continue iteration
data remove storage mgs:temp _wb_iter[0]
execute if data storage mgs:temp _wb_iter[0] run function mgs:v5.0.0/zombies/wallbuys/setup_iter

