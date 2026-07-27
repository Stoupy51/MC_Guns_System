""" Wallbuy scoreboards and summoning each buy's interaction and item display. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .....config.stats.keys import GRENADE_TYPE


# Functions
def write_wallbuy_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Wallbuy entity scoreboards
	write_load_file(f"""
# Wallbuy entity scoreboards
scoreboard objectives add {ns}.zb.wb.id dummy
scoreboard objectives add {ns}.zb.wb.price dummy
scoreboard objectives add {ns}.zb.wb.rfprice dummy
scoreboard objectives add {ns}.zb.wb.rfpap dummy
""")

	## Setup: iterate wallbuy compounds, summon interaction + item_display entities
	write_versioned_function("zombies/wallbuys/setup", f"""
scoreboard players set #wb_counter {ns}.data 0
data modify storage {ns}:zombies wallbuy_data set value {{}}
data modify storage {ns}:temp _wb_iter set from storage {ns}:zombies game.map.wallbuys
execute if data storage {ns}:temp _wb_iter[0] run function {ns}:v{version}/zombies/wallbuys/setup_iter
""")

	write_versioned_function("zombies/wallbuys/setup_iter", f"""
# Assign incrementing ID
scoreboard players add #wb_counter {ns}.data 1

# Read relative position and convert to absolute
execute store result score #wbx {ns}.data run data get storage {ns}:temp _wb_iter[0].pos[0]
execute store result score #wby {ns}.data run data get storage {ns}:temp _wb_iter[0].pos[1]
execute store result score #wbz {ns}.data run data get storage {ns}:temp _wb_iter[0].pos[2]
scoreboard players operation #wbx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #wby {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #wbz {ns}.data += #gm_base_z {ns}.data

# Store absolute position and weapon_id for macro
execute store result storage {ns}:temp _wb.x int 1 run scoreboard players get #wbx {ns}.data
execute store result storage {ns}:temp _wb.y int 1 run scoreboard players get #wby {ns}.data
execute store result storage {ns}:temp _wb.z int 1 run scoreboard players get #wbz {ns}.data
data modify storage {ns}:temp _wb.weapon_id set from storage {ns}:temp _wb_iter[0].weapon_id

# Read display name (default to weapon_id, override with "name" field)
data modify storage {ns}:temp _wb.name set from storage {ns}:temp _wb_iter[0].weapon_id
execute if data storage {ns}:temp _wb_iter[0].name run data modify storage {ns}:temp _wb.name set from storage {ns}:temp _wb_iter[0].name

# Read rotation
data modify storage {ns}:temp _wb.rotation set from storage {ns}:temp _wb_iter[0].rotation

# Summon interaction + item display entities
function {ns}:v{version}/zombies/wallbuys/place_at with storage {ns}:temp _wb
execute as @n[tag={ns}.wb_new] at @s run tp @s ^ ^ ^-0.5
execute as @n[tag={ns}.wb_new_display] at @s run tp @s ^ ^0.5 ^-0.49

# Set scoreboards on interaction entity
scoreboard players operation @n[tag={ns}.wb_new] {ns}.zb.wb.id = #wb_counter {ns}.data
execute store result score @n[tag={ns}.wb_new] {ns}.zb.wb.price run data get storage {ns}:temp _wb_iter[0].price
execute store result score @n[tag={ns}.wb_new] {ns}.zb.wb.rfprice run data get storage {ns}:temp _wb_iter[0].refill_price
execute store result score @n[tag={ns}.wb_new] {ns}.zb.wb.rfpap run data get storage {ns}:temp _wb_iter[0].refill_price_pap

# Store weapon_id, magazine_id, and name in indexed storage for later lookup
# (magazine_id is optional on non-gun wallbuys: pre-clear so a missing field can't leak the
# previous iteration's value)
execute store result storage {ns}:temp _wb_store.id int 1 run scoreboard players get #wb_counter {ns}.data
data modify storage {ns}:temp _wb_store.weapon_id set from storage {ns}:temp _wb_iter[0].weapon_id
data modify storage {ns}:temp _wb_store.magazine_id set value ""
data modify storage {ns}:temp _wb_store.magazine_id set from storage {ns}:temp _wb_iter[0].magazine_id
data modify storage {ns}:temp _wb_store.name set from storage {ns}:temp _wb.name

# Register Bookshelf events
execute as @n[tag={ns}.wb_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/wallbuys/on_right_click",executor:"source"}}
execute as @n[tag={ns}.wb_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/wallbuys/on_hover",executor:"source"}}
tag @n[tag={ns}.wb_new] remove {ns}.wb_new

# Set item on display entity
function {ns}:v{version}/zombies/wallbuys/set_display_item with storage {ns}:temp _wb

# Capture displayed item_name for hover title
data modify storage {ns}:temp _wb_store.item_name set from entity @n[tag={ns}.wb_new_display] item.components."minecraft:item_name"

# Probe the item KIND from the display item's custom_data (0 gun, 1 knife, 2 lethal, 3 tactical).
# Grenade check first so the tactical flag can override it (monkey bombs carry both).
scoreboard players set #wb_kind {ns}.data 0
execute if data entity @n[tag={ns}.wb_new_display] item.components."minecraft:custom_data".{ns}.stats.{GRENADE_TYPE} run scoreboard players set #wb_kind {ns}.data 2
execute if data entity @n[tag={ns}.wb_new_display] item.components."minecraft:custom_data".{ns}.tactical run scoreboard players set #wb_kind {ns}.data 3
execute if data entity @n[tag={ns}.wb_new_display] item.components."minecraft:custom_data".{ns}.knife run scoreboard players set #wb_kind {ns}.data 1
execute store result storage {ns}:temp _wb_store.kind int 1 run scoreboard players get #wb_kind {ns}.data
function {ns}:v{version}/zombies/wallbuys/store_data with storage {ns}:temp _wb_store

tag @e[tag={ns}.wb_new_display] remove {ns}.wb_new_display

# Continue iteration
data remove storage {ns}:temp _wb_iter[0]
execute if data storage {ns}:temp _wb_iter[0] run function {ns}:v{version}/zombies/wallbuys/setup_iter
""")

	write_versioned_function("zombies/wallbuys/place_at", f"""
# Summon interaction entity slightly in front of the wall, centered on display height.
$summon minecraft:interaction $(x) $(y) $(z) {{width:0.9f,height:1.0f,response:true,Rotation:$(rotation),Tags:["{ns}.wallbuy","{ns}.gm_entity","bs.entity.interaction","{ns}.wb_new"]}}

# Summon item display offset toward the wall face.
$summon minecraft:item_display $(x) $(y) $(z) {{billboard:"fixed",item_display:"fixed",Rotation:$(rotation),Tags:["{ns}.wallbuy_display","{ns}.gm_entity","{ns}.wb_new_display"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}
""")

	write_versioned_function("zombies/wallbuys/store_data", f"""
$data modify storage {ns}:zombies wallbuy_data."$(id)" set value {{weapon_id:"$(weapon_id)",name:"$(name)",magazine_id:"$(magazine_id)",kind:$(kind),item_name:$(item_name)}}
""")

	write_versioned_function("zombies/wallbuys/set_display_item", f"""
$execute as @e[tag={ns}.wb_new_display] run loot replace entity @s contents loot {ns}:i/$(weapon_id)
""")

