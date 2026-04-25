# ruff: noqa: E501
# Wallbuy System
# Wall-mounted weapon stations. Players interact to buy weapons.
# Each wallbuy displays its weapon on the wall and shows info on hover.
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from .common import build_weapon_magazine_data, deny_not_enough_points_body, game_active_guard_cmd


def generate_wallbuys() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	gun_cd: str = "{" + ns + ":{gun:true}}"
	mag_cd: str = "{" + ns + ":{magazine:true}}"
	wallbuy_hover_message: str = (
		f'[{{"text":"🔫 ","color":"gold"}},'
		f'{{"storage":"{ns}:temp","nbt":"_wb_display_name","color":"yellow","interpret":true}},'
		f'{{"text":" - Cost: ","color":"gray"}},'
		f'{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":" points","color":"gray"}},'
		f'{{"storage":"{ns}:temp","nbt":"_wb_price_suffix","color":"gray","interpret":true}}]'
	)

	# Build weapon_id -> magazine_id mapping
	weapon_mag_data: dict[str, str] = {}
	for weapon_id, (mag_id, _, _) in build_weapon_magazine_data().items():
		weapon_mag_data[weapon_id] = mag_id

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
execute store result storage {ns}:temp _wb_store.id int 1 run scoreboard players get #wb_counter {ns}.data
data modify storage {ns}:temp _wb_store.weapon_id set from storage {ns}:temp _wb_iter[0].weapon_id
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
$data modify storage {ns}:zombies wallbuy_data."$(id)" set value {{weapon_id:"$(weapon_id)",name:"$(name)",magazine_id:"$(magazine_id)",item_name:$(item_name)}}
""")

	write_versioned_function("zombies/wallbuys/set_display_item", f"""
$execute as @e[tag={ns}.wb_new_display] run loot replace entity @s contents loot {ns}:i/$(weapon_id)
""")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/wallbuys/on_right_click", f"""
# Guard: game must be active
{game_active_guard_cmd(ns)}

# Get wallbuy id + data first (used by dynamic price logic)
execute store result storage {ns}:temp _wb_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.id
function {ns}:v{version}/zombies/wallbuys/lookup_weapon with storage {ns}:temp _wb_buy
function {ns}:v{version}/zombies/wallbuys/get_display_name

# Read all possible prices from wallbuy entity
execute store result score #wb_buy_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.price
execute store result score #wb_rfprice {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfprice
execute store result score #wb_rfpap {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfpap

# Compute effective price for this interaction (buy vs refill vs PAP refill)
scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
function {ns}:v{version}/zombies/wallbuys/compute_effective_price with storage {ns}:temp _wb_weapon

# Check player has enough points
execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run function {ns}:v{version}/zombies/wallbuys/deny_not_enough_points

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data

# Process buy by zombies inventory rules
function {ns}:v{version}/zombies/wallbuys/process_purchase with storage {ns}:temp _wb_weapon

execute if score #wb_purchase_mode {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/msg_purchased
execute if score #wb_purchase_mode {ns}.data matches 2 run function {ns}:v{version}/zombies/wallbuys/msg_refilled
execute if score #wb_purchase_mode {ns}.data matches 3 run function {ns}:v{version}/zombies/wallbuys/msg_replaced
execute if score #wb_purchase_mode {ns}.data matches 4 run scoreboard players operation @s {ns}.zb.points += #wb_price {ns}.data
execute if score #wb_purchase_mode {ns}.data matches 4 run function {ns}:v{version}/zombies/wallbuys/msg_refund_full
""")

	write_versioned_function("zombies/wallbuys/deny_not_enough_points", f"""
{deny_not_enough_points_body(ns, version, "#wb_price")}
""")

	write_versioned_function("zombies/wallbuys/msg_purchased", f"""
tellraw @s [{MGS_TAG},{{"text":"You bought ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_wb_display_name","color":"gold","interpret":true}},{{"text":" for ","color":"green"}},{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points.","color":"green"}}]
function {ns}:v{version}/zombies/feedback/sound_success
""")

	write_versioned_function("zombies/wallbuys/msg_refilled", f"""
tellraw @s [{MGS_TAG},{{"text":"Ammo refilled for ","color":"gold"}},{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points.","color":"gold"}}]
function {ns}:v{version}/zombies/feedback/sound_refill
""")

	write_versioned_function("zombies/wallbuys/msg_replaced", f"""
tellraw @s [{MGS_TAG},{{"text":"Swapped your selected weapon for ","color":"yellow"}},{{"storage":"{ns}:temp","nbt":"_wb_display_name","color":"gold","interpret":true}},{{"text":" (","color":"yellow"}},{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points).","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_replace
""")

	write_versioned_function("zombies/wallbuys/msg_refund_full", f"""
tellraw @s [{MGS_TAG},{{"text":"Ammo is already full. Refunded ","color":"red"}},{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	# Generate lookup function for weapon -> magazine mapping
	magazine_lookup_cmds = "\n".join([
		f"execute if data storage {ns}:temp _wb_store{{weapon_id:\"{wid}\"}} run data modify storage {ns}:temp _wb_store.magazine_id set value \"{mag_id}\""
		for wid, (mag_id, _, _) in build_weapon_magazine_data().items()
	])

	write_versioned_function("zombies/wallbuys/lookup_magazine_id", f"""
{magazine_lookup_cmds}
""")

	write_versioned_function("zombies/wallbuys/lookup_weapon", f"""
$data modify storage {ns}:temp _wb_weapon set from storage {ns}:zombies wallbuy_data."$(id)"
""")

	write_versioned_function("zombies/wallbuys/get_display_name", f"""
# Default to localized display item name.
data modify storage {ns}:temp _wb_display_name set from storage {ns}:temp _wb_weapon.item_name

# If a custom map name is set, use it instead.
execute unless data storage {ns}:temp _wb_weapon{{name:""}} if data storage {ns}:temp _wb_weapon.name run data modify storage {ns}:temp _wb_display_name set from storage {ns}:temp _wb_weapon.name
""")

	write_versioned_function("zombies/wallbuys/process_purchase", f"""
scoreboard players set #wb_purchase_done {ns}.data 0
scoreboard players set #wb_purchase_mode {ns}.data 0

# Always prioritize refill of the same weapon to prevent duplicates.
execute if score #wb_purchase_done {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/try_refill_owned with storage {ns}:temp _wb_weapon

# New placement: give to the first empty gun slot (checks each slot individually)
$execute if score #wb_purchase_done {ns}.data matches 0 unless items entity @s hotbar.1 *[custom_data~{gun_cd}] run function {ns}:v{version}/zombies/wallbuys/give_to_slot {{hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 unless items entity @s hotbar.2 *[custom_data~{gun_cd}] run function {ns}:v{version}/zombies/wallbuys/give_to_slot {{hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 unless items entity @s hotbar.3 *[custom_data~{gun_cd}] if score @s {ns}.zb.perk.mule_kick matches 1.. run function {ns}:v{version}/zombies/wallbuys/give_to_slot {{hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}

# Otherwise replace the currently selected gun slot (1/2/3 only)
execute if score #wb_purchase_done {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/replace_selected with storage {ns}:temp _wb_weapon
""")

	write_versioned_function("zombies/wallbuys/count_guns", f"""
scoreboard players set #wb_gun_count {ns}.data 0
execute if items entity @s hotbar.1 *[custom_data~{gun_cd}] run scoreboard players add #wb_gun_count {ns}.data 1
execute if items entity @s hotbar.2 *[custom_data~{gun_cd}] run scoreboard players add #wb_gun_count {ns}.data 1
execute if items entity @s hotbar.3 *[custom_data~{gun_cd}] run scoreboard players add #wb_gun_count {ns}.data 1
""")

	write_versioned_function("zombies/wallbuys/give_to_slot", f"""
$loot replace entity @s hotbar.$(hotbar) loot {ns}:i/$(weapon_id)

scoreboard players set #wb_mag_given {ns}.data 0
$execute store success score #wb_mag_given {ns}.data run loot replace entity @s inventory.$(inventory) loot {ns}:i/$(magazine_id)
$execute if score #wb_mag_given {ns}.data matches 0 run item replace entity @s inventory.$(inventory) with air

$function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}}
$execute if score #wb_mag_given {ns}.data matches 1 run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}}
$execute if score #wb_mag_given {ns}.data matches 1 run function {ns}:v{version}/zombies/inventory/scale_magazine_slot {{slot:"inventory.$(inventory)",index:$(inventory),remaining_multiplier:1}}

$function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"hotbar.$(hotbar)"}}

scoreboard players set #wb_purchase_done {ns}.data 1
scoreboard players set #wb_purchase_mode {ns}.data 1
""")

	write_versioned_function("zombies/wallbuys/try_refill_owned", f"""
execute if score #wb_purchase_done {ns}.data matches 1 run return 0

function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.1"}}
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:1,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full

function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.2"}}
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:2,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full

function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.3"}}
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:3,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full
""")

	write_versioned_function("zombies/wallbuys/refill_already_full", f"""
scoreboard players set #wb_purchase_done {ns}.data 1
scoreboard players set #wb_purchase_mode {ns}.data 4
""")

	write_versioned_function("zombies/wallbuys/compute_effective_price", f"""
scoreboard players set #wb_price_locked {ns}.data 0
scoreboard players set #wb_price_mode {ns}.data 0

# Slot 1 refill candidate
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:1,weapon_id:"$(weapon_id)"}}
execute if score #wb_same_weapon {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.1"}}
execute if score #wb_price_locked {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run return run function {ns}:v{version}/zombies/wallbuys/select_refill_price {{hotbar:1}}

# Slot 2 refill candidate
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:2,weapon_id:"$(weapon_id)"}}
execute if score #wb_same_weapon {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.2"}}
execute if score #wb_price_locked {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run return run function {ns}:v{version}/zombies/wallbuys/select_refill_price {{hotbar:2}}

# Slot 3 refill candidate
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:3,weapon_id:"$(weapon_id)"}}
execute if score #wb_same_weapon {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.3"}}
execute if score #wb_price_locked {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run return run function {ns}:v{version}/zombies/wallbuys/select_refill_price {{hotbar:3}}
""")

	write_versioned_function("zombies/wallbuys/select_refill_price", f"""
# Default refill price
scoreboard players operation #wb_price {ns}.data = #wb_rfprice {ns}.data
scoreboard players set #wb_price_mode {ns}.data 1

# PAP refill price if weapon in this slot has pap_level > 0
scoreboard players set #wb_pap_level {ns}.data 0
$execute store result score #wb_pap_level {ns}.data run data get entity @s Inventory[{{Slot:$(hotbar)b}}].components."minecraft:custom_data".{ns}.stats.pap_level
execute if score #wb_pap_level {ns}.data matches 1.. run scoreboard players operation #wb_price {ns}.data = #wb_rfpap {ns}.data
execute if score #wb_pap_level {ns}.data matches 1.. run scoreboard players set #wb_price_mode {ns}.data 2

scoreboard players set #wb_price_locked {ns}.data 1
""")

	write_versioned_function("zombies/wallbuys/set_hover_price_suffix", f"""
data modify storage {ns}:temp _wb_price_suffix set value ""
execute if score #wb_price_mode {ns}.data matches 1 run data modify storage {ns}:temp _wb_price_suffix set value " (Refill)"
execute if score #wb_price_mode {ns}.data matches 2 run data modify storage {ns}:temp _wb_price_suffix set value " (PAP Refill)"
""")

	write_versioned_function("zombies/wallbuys/check_mag_not_full", f"""
scoreboard players set #wb_mag_not_full {ns}.data 0

# Missing paired mag counts as not full.
$execute unless items entity @s $(slot) *[custom_data~{mag_cd}] run scoreboard players set #wb_mag_not_full {ns}.data 1

tag @s add {ns}.wb_reading_mag
$execute if items entity @s $(slot) *[custom_data~{mag_cd}] summon minecraft:item_display run function {ns}:v{version}/zombies/wallbuys/read_mag_state {{slot:"$(slot)"}}
tag @s remove {ns}.wb_reading_mag

execute if score #wb_mag_rem {ns}.data < #wb_mag_cap {ns}.data run scoreboard players set #wb_mag_not_full {ns}.data 1
""")

	write_versioned_function("zombies/wallbuys/check_same_weapon_slot", f"""
scoreboard players set #wb_same_weapon {ns}.data 0
$execute store success score #wb_same_weapon {ns}.data run data get entity @s Inventory[{{Slot:$(slot)b}}].components."minecraft:custom_data".{ns}.$(weapon_id)
""")

	write_versioned_function("zombies/wallbuys/read_mag_state", f"""
$item replace entity @s contents from entity @p[tag={ns}.wb_reading_mag] $(slot)
execute store result score #wb_mag_rem {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.remaining_bullets
execute store result score #wb_mag_cap {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.capacity
kill @s
""")

	write_versioned_function("zombies/wallbuys/reload_pair", f"""
scoreboard players set #wb_new_mag {ns}.data 0
scoreboard players set #wb_mag_created {ns}.data 0
$execute unless items entity @s inventory.$(inventory) *[custom_data~{mag_cd}] run scoreboard players set #wb_new_mag {ns}.data 1
$execute if score #wb_new_mag {ns}.data matches 1 store success score #wb_mag_created {ns}.data run loot replace entity @s inventory.$(inventory) loot {ns}:i/$(magazine_id)
$execute if score #wb_new_mag {ns}.data matches 1 if score #wb_mag_created {ns}.data matches 1 run function {ns}:v{version}/zombies/inventory/scale_magazine_slot {{slot:"inventory.$(inventory)",index:$(inventory),remaining_multiplier:1}}

$function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"hotbar.$(hotbar)"}}
$execute if items entity @s inventory.$(inventory) *[custom_data~{mag_cd}] run function {ns}:v{version}/zombies/bonus/refill_magazine {{slot:"inventory.$(inventory)"}}

$function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}}
$execute if items entity @s inventory.$(inventory) *[custom_data~{mag_cd}] run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}}

scoreboard players set #wb_purchase_done {ns}.data 1
scoreboard players set #wb_purchase_mode {ns}.data 2
""")

	write_versioned_function("zombies/wallbuys/replace_selected", f"""
scoreboard players set #wb_valid_sel {ns}.data 0
execute store result score #wb_sel {ns}.data run data get entity @s SelectedItemSlot

execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.1"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:1,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 1 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 1 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 1 if items entity @s hotbar.1 *[custom_data~{gun_cd}] run function {ns}:v{version}/zombies/wallbuys/replace_pair {{hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}

execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 2 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.2"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 2 run function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:2,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 2 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 2 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 2 if items entity @s hotbar.2 *[custom_data~{gun_cd}] run function {ns}:v{version}/zombies/wallbuys/replace_pair {{hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}

execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 3 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.3"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 3 run function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:3,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 3 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 3 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 3 if items entity @s hotbar.3 *[custom_data~{gun_cd}] run function {ns}:v{version}/zombies/wallbuys/replace_pair {{hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}

execute if score #wb_purchase_done {ns}.data matches 0 run scoreboard players operation @s {ns}.zb.points += #wb_price {ns}.data
execute if score #wb_purchase_done {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/deny_hold_valid_slot
execute if score #wb_purchase_done {ns}.data matches 0 run scoreboard players set #wb_purchase_mode {ns}.data -1
""")

	write_versioned_function("zombies/wallbuys/deny_hold_valid_slot", f"""
execute if score @s {ns}.zb.perk.mule_kick matches 1.. run tellraw @s [{MGS_TAG},{{"text":"Hold weapon slot 1, 2, or 3 to swap your current gun.","color":"red"}}]
execute unless score @s {ns}.zb.perk.mule_kick matches 1.. run tellraw @s [{MGS_TAG},{{"text":"Hold weapon slot 1 or 2 to swap your current gun.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/wallbuys/replace_pair", f"""
$loot replace entity @s hotbar.$(hotbar) loot {ns}:i/$(weapon_id)

scoreboard players set #wb_mag_given {ns}.data 0
$execute store success score #wb_mag_given {ns}.data run loot replace entity @s inventory.$(inventory) loot {ns}:i/$(magazine_id)
$execute if score #wb_mag_given {ns}.data matches 0 run item replace entity @s inventory.$(inventory) with air

$function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}}
$execute if score #wb_mag_given {ns}.data matches 1 run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}}
$execute if score #wb_mag_given {ns}.data matches 1 run function {ns}:v{version}/zombies/inventory/scale_magazine_slot {{slot:"inventory.$(inventory)",index:$(inventory),remaining_multiplier:1}}

$function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"hotbar.$(hotbar)"}}

scoreboard players set #wb_purchase_done {ns}.data 1
scoreboard players set #wb_purchase_mode {ns}.data 3
""")

	## Hover events (executor: "source" = player)
	write_versioned_function("zombies/wallbuys/get_hover_name", f"""
$data modify storage {ns}:temp _wb_weapon set from storage {ns}:zombies wallbuy_data."$(id)"
""")

	write_versioned_function("zombies/wallbuys/render_hover_title", f"""
title @s title [{{"text":"🔫 ","color":"gold"}},{{"storage":"{ns}:temp","nbt":"_wb_weapon.item_name","color":"gold","interpret":true}}]
""")

	write_versioned_function("zombies/wallbuys/on_hover", f"""
execute store result storage {ns}:temp _wb_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.id
function {ns}:v{version}/zombies/wallbuys/get_hover_name with storage {ns}:temp _wb_hover
function {ns}:v{version}/zombies/wallbuys/get_display_name

# Dynamic hover price (buy, refill, or PAP refill)
execute store result score #wb_buy_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.price
execute store result score #wb_rfprice {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfprice
execute store result score #wb_rfpap {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfpap
scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
function {ns}:v{version}/zombies/wallbuys/compute_effective_price with storage {ns}:temp _wb_weapon
function {ns}:v{version}/zombies/wallbuys/set_hover_price_suffix

data modify storage smithed.actionbar:input message set value {{json:{wallbuy_hover_message},priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	## Hook into preload_complete: setup wallbuys
	write_versioned_function("zombies/preload_complete", f"""
# Setup wallbuys
execute if data storage {ns}:zombies game.map.wallbuys[0] run function {ns}:v{version}/zombies/wallbuys/setup
""")

