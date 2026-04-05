
#> mgs:v5.0.0/zombies/pap/setup_iter
#
# @within	mgs:v5.0.0/zombies/pap/setup
#			mgs:v5.0.0/zombies/pap/setup_iter
#

# Assign incrementing machine id
scoreboard players add #pap_counter mgs.data 1

# Convert relative map coords to absolute world coords
execute store result score #papx mgs.data run data get storage mgs:temp _pap_iter[0].pos[0]
execute store result score #papy mgs.data run data get storage mgs:temp _pap_iter[0].pos[1]
execute store result score #papz mgs.data run data get storage mgs:temp _pap_iter[0].pos[2]
scoreboard players operation #papx mgs.data += #gm_base_x mgs.data
scoreboard players operation #papy mgs.data += #gm_base_y mgs.data
scoreboard players operation #papz mgs.data += #gm_base_z mgs.data

# Store absolute coords for summon macro
execute store result storage mgs:temp _pap_place.x int 1 run scoreboard players get #papx mgs.data
execute store result storage mgs:temp _pap_place.y int 1 run scoreboard players get #papy mgs.data
execute store result storage mgs:temp _pap_place.z int 1 run scoreboard players get #papz mgs.data

# Summon interaction entity
function mgs:v5.0.0/zombies/pap/place_at with storage mgs:temp _pap_place

# Set machine metadata
scoreboard players operation @n[tag=mgs.pap_new] mgs.zb.pap.id = #pap_counter mgs.data
execute store result score @n[tag=mgs.pap_new] mgs.zb.pap.price run data get storage mgs:temp _pap_iter[0].price
execute store result score @n[tag=mgs.pap_new] mgs.zb.pap.power run data get storage mgs:temp _pap_iter[0].power

# Register Bookshelf interaction callbacks
execute as @n[tag=mgs.pap_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.0/zombies/pap/on_right_click",executor:"source"}
execute as @n[tag=mgs.pap_new] run function #bs.interaction:on_hover {run:"function mgs:v5.0.0/zombies/pap/on_hover",executor:"source"}

# Initialize animation state: -1 = idle
scoreboard players set @n[tag=mgs.pap_new] mgs.pap_anim -1

# Spawn visual item_display at machine position (default: netherite_block; overridable via display_item + item_model map fields)
data modify storage mgs:temp _pap_disp.tag set value "mgs.pap_display"
data modify storage mgs:temp _pap_disp.item_id set value "minecraft:netherite_block"
data modify storage mgs:temp _pap_disp.item_model set value "minecraft:netherite_block"
execute if data storage mgs:temp _pap_iter[0].display_item run data modify storage mgs:temp _pap_disp.item_id set from storage mgs:temp _pap_iter[0].display_item
execute if data storage mgs:temp _pap_iter[0].item_model run data modify storage mgs:temp _pap_disp.item_model set from storage mgs:temp _pap_iter[0].item_model
execute as @n[tag=mgs.pap_new] at @s run function mgs:v5.0.0/zombies/display/summon_machine_display with storage mgs:temp _pap_disp

# Store display metadata for lookup (reuse the computed _pap_disp fields)
execute store result storage mgs:temp _pap_store.id int 1 run scoreboard players get #pap_counter mgs.data
data modify storage mgs:temp _pap_store.name set value "Pack-a-Punch"
execute if data storage mgs:temp _pap_iter[0].name run data modify storage mgs:temp _pap_store.name set from storage mgs:temp _pap_iter[0].name
data modify storage mgs:temp _pap_store.display_tag set from storage mgs:temp _pap_disp.tag
data modify storage mgs:temp _pap_store.display_item_id set from storage mgs:temp _pap_disp.item_id
data modify storage mgs:temp _pap_store.display_item_model set from storage mgs:temp _pap_disp.item_model
function mgs:v5.0.0/zombies/pap/store_data with storage mgs:temp _pap_store

tag @n[tag=mgs.pap_new] remove mgs.pap_new

# Continue iteration
data remove storage mgs:temp _pap_iter[0]
execute if data storage mgs:temp _pap_iter[0] run function mgs:v5.0.0/zombies/pap/setup_iter

