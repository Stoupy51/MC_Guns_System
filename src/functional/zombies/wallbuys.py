
# ruff: noqa: E501
# Wallbuy System
# Wall-mounted weapon stations. Players interact to buy weapons.
# Each wallbuy displays its weapon on the wall and shows info on hover.
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG


def generate_wallbuys() -> None:
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

# Read facing (default 0 = south)
data modify storage {ns}:temp _wb.facing set value 0
execute store result storage {ns}:temp _wb.facing int 1 run data get storage {ns}:temp _wb_iter[0].facing

# Summon interaction + item display entities
function {ns}:v{version}/zombies/wallbuys/place_at with storage {ns}:temp _wb

# Set scoreboards on interaction entity
scoreboard players operation @n[tag=_wb_new] {ns}.zb.wb.id = #wb_counter {ns}.data
execute store result score @n[tag=_wb_new] {ns}.zb.wb.price run data get storage {ns}:temp _wb_iter[0].price
execute store result score @n[tag=_wb_new] {ns}.zb.wb.rfprice run data get storage {ns}:temp _wb_iter[0].refill_price
execute store result score @n[tag=_wb_new] {ns}.zb.wb.rfpap run data get storage {ns}:temp _wb_iter[0].refill_price_pap

# Store weapon_id in indexed storage for later lookup
execute store result storage {ns}:temp _wb_store.id int 1 run scoreboard players get #wb_counter {ns}.data
data modify storage {ns}:temp _wb_store.weapon_id set from storage {ns}:temp _wb_iter[0].weapon_id
data modify storage {ns}:temp _wb_store.name set from storage {ns}:temp _wb.name
function {ns}:v{version}/zombies/wallbuys/store_data with storage {ns}:temp _wb_store

# Register Bookshelf events
execute as @n[tag=_wb_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/wallbuys/on_right_click",executor:"source"}}
execute as @n[tag=_wb_new] run function #bs.interaction:on_hover_enter {{run:"function {ns}:v{version}/zombies/wallbuys/on_hover_enter",executor:"source"}}
execute as @n[tag=_wb_new] run function #bs.interaction:on_hover_leave {{run:"function {ns}:v{version}/zombies/wallbuys/on_hover_leave",executor:"source"}}
tag @n[tag=_wb_new] remove _wb_new

# Set item on display entity
function {ns}:v{version}/zombies/wallbuys/set_display_item with storage {ns}:temp _wb
tag @e[tag={ns}.wb_new_display] remove {ns}.wb_new_display

# Continue iteration
data remove storage {ns}:temp _wb_iter[0]
execute if data storage {ns}:temp _wb_iter[0] run function {ns}:v{version}/zombies/wallbuys/setup_iter
""")

	write_versioned_function("zombies/wallbuys/place_at", f"""
# Summon interaction entity
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.0f,height:1.0f,response:true,Tags:["{ns}.wallbuy","{ns}.gm_entity","bs.entity.interaction","_wb_new"]}}

# Summon item display (fixed to wall)
$summon minecraft:item_display $(x) $(y) $(z) {{billboard:"fixed",Rotation:[$(facing)f,0f],Tags:["{ns}.wallbuy_display","{ns}.gm_entity","{ns}.wb_new_display"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.5f,0f],scale:[0.6f,0.6f,0.6f]}}}}
""")

	write_versioned_function("zombies/wallbuys/store_data", f"""
$data modify storage {ns}:zombies wallbuy_data."$(id)" set value {{weapon_id:"$(weapon_id)",name:"$(name)"}}
""")

	write_versioned_function("zombies/wallbuys/set_display_item", f"""
$execute as @e[tag={ns}.wb_new_display] run loot replace entity @s contents loot {ns}:i/$(weapon_id)
""")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/wallbuys/on_right_click", f"""
# Guard: game must be active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# Get wallbuy price
execute store result score #wb_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.price

# Check player has enough points
execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run tellraw @s [{MGS_TAG},{{"text":" Not enough points!","color":"red"}}]

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data

# Get weapon_id from storage via wallbuy ID
execute store result storage {ns}:temp _wb_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.id
function {ns}:v{version}/zombies/wallbuys/lookup_weapon with storage {ns}:temp _wb_buy

# Give weapon to player
function {ns}:v{version}/zombies/wallbuys/give_weapon with storage {ns}:temp _wb_weapon

# Announce
tellraw @s [{MGS_TAG},{{"text":" Weapon purchased!","color":"green"}}]
""")

	write_versioned_function("zombies/wallbuys/lookup_weapon", f"""
$data modify storage {ns}:temp _wb_weapon set from storage {ns}:zombies wallbuy_data."$(id)"
""")

	write_versioned_function("zombies/wallbuys/give_weapon", f"""
$loot give @s loot {ns}:i/$(weapon_id)
""")

	## Hover events (executor: "source" = player)
	write_versioned_function("zombies/wallbuys/get_hover_name", f"""
$data modify storage {ns}:temp wb_hover_name set from storage {ns}:zombies wallbuy_data."$(id)".name
""")

	write_versioned_function("zombies/wallbuys/on_hover_enter", f"""
execute store result score #wb_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.price
execute store result storage {ns}:temp _wb_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.id
function {ns}:v{version}/zombies/wallbuys/get_hover_name with storage {ns}:temp _wb_hover
title @s times 0 40 10
title @s title [{{"text":"🔫 ","color":"gold"}},{{"storage":"{ns}:temp","nbt":"wb_hover_name","color":"gold"}}]
title @s subtitle [{{"text":"Cost: ","color":"gray"}},{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}]
""")

	write_versioned_function("zombies/wallbuys/on_hover_leave", """
title @s clear
""")

	## Hook into preload_complete: setup wallbuys
	write_versioned_function("zombies/preload_complete", f"""
# Setup wallbuys
execute if data storage {ns}:zombies game.map.wallbuys[0] run function {ns}:v{version}/zombies/wallbuys/setup
""")
