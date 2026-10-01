""" Perk machine objectives and placing one interaction entity plus model per map position. """
# Imports
from stewbeet import Mem, write_load_file, write_tag, write_versioned_function

from .definitions import PERK_DEFINITIONS, RECOMMENDED_PRICES


# Functions
def write_perk_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	perk_objectives_add: str = "\n".join(
		f"scoreboard objectives add {ns}.zb.perk.{perk_id} dummy"
		for perk_id in PERK_DEFINITIONS
	)

	# Chip-in progress is per player, so it lives and clears with the ownership objectives.
	perkpaid_objectives_add: str = "\n".join(
		f"scoreboard objectives add {ns}.zb.perkpaid.{perk_id} dummy"
		for perk_id in PERK_DEFINITIONS
	)

	write_load_file(f"""
scoreboard objectives add {ns}.zb.perk.id dummy
scoreboard objectives add {ns}.zb.perk.price dummy
# Kept so dynamic discounts (solo Quick Revive) can be reverted.
scoreboard objectives add {ns}.zb.perk.base_price dummy
scoreboard objectives add {ns}.zb.perk.power dummy
# 0 = buy in one payment.
scoreboard objectives add {ns}.zb.perk.partial dummy

{perk_objectives_add}

{perkpaid_objectives_add}
""")

	write_tag("zombies/on_new_perk", Mem.ctx.data[ns].function_tags, [])

	write_versioned_function("zombies/perks/setup", f"""
scoreboard players set #pk_counter {ns}.data 0
data modify storage {ns}:zombies perk_data set value {{}}
data modify storage {ns}:temp _pk_iter set from storage {ns}:zombies game.map.perks
execute if data storage {ns}:temp _pk_iter[0] run function {ns}:v{version}/zombies/perks/setup_iter
""")

	# A map price of -1 means the recommended price of the perk_id.
	price_resolve_lines: str = "\n".join(
		f'execute if score @n[tag={ns}.pk_new] {ns}.zb.perk.price matches -1 if data storage {ns}:temp _pk_price{{perk_id:"{perk_id}"}} run scoreboard players set @n[tag={ns}.pk_new] {ns}.zb.perk.price {RECOMMENDED_PRICES.get(perk_id, 2000)}'
		for perk_id in PERK_DEFINITIONS
	)
	write_versioned_function("zombies/perks/setup_iter", f"""
scoreboard players add #pk_counter {ns}.data 1

execute store result score #pkx {ns}.data run data get storage {ns}:temp _pk_iter[0].pos[0]
execute store result score #pky {ns}.data run data get storage {ns}:temp _pk_iter[0].pos[1]
execute store result score #pkz {ns}.data run data get storage {ns}:temp _pk_iter[0].pos[2]
scoreboard players operation #pkx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #pky {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #pkz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _pk.x int 1 run scoreboard players get #pkx {ns}.data
execute store result storage {ns}:temp _pk.y int 1 run scoreboard players get #pky {ns}.data
execute store result storage {ns}:temp _pk.z int 1 run scoreboard players get #pkz {ns}.data
data modify storage {ns}:temp _pk.rotation set from storage {ns}:temp _pk_iter[0].rotation

function {ns}:v{version}/zombies/perks/place_at with storage {ns}:temp _pk

scoreboard players operation @n[tag={ns}.pk_new] {ns}.zb.perk.id = #pk_counter {ns}.data
execute store result score @n[tag={ns}.pk_new] {ns}.zb.perk.price run data get storage {ns}:temp _pk_iter[0].price
# Copied to a flat key first: `[0]{{...}}` after an index is invalid NBT path syntax.
data modify storage {ns}:temp _pk_price.perk_id set from storage {ns}:temp _pk_iter[0].perk_id
{price_resolve_lines}
scoreboard players operation @n[tag={ns}.pk_new] {ns}.zb.perk.base_price = @n[tag={ns}.pk_new] {ns}.zb.perk.price
# Quick Revive machines get dynamic solo pricing.
data modify storage {ns}:temp _pk_qr.perk_id set from storage {ns}:temp _pk_iter[0].perk_id
execute if data storage {ns}:temp _pk_qr{{perk_id:"quick_revive"}} run tag @n[tag={ns}.pk_new] add {ns}.pk_quick_revive
# true is stored as 1b, so `data get` returns 1.
execute store result score @n[tag={ns}.pk_new] {ns}.zb.perk.power run data get storage {ns}:temp _pk_iter[0].power
# Maps saved before chip-in existed have no field: the failed read stores 0 (off).
execute store result score @n[tag={ns}.pk_new] {ns}.zb.perk.partial run data get storage {ns}:temp _pk_iter[0].partial_price

execute store result storage {ns}:temp _pk_store.id int 1 run scoreboard players get #pk_counter {ns}.data
data modify storage {ns}:temp _pk_store.perk_id set from storage {ns}:temp _pk_iter[0].perk_id
# A custom label is kept only when non-empty; otherwise the perk's display_name is used.
data remove storage {ns}:temp _pk_store.name
data modify storage {ns}:temp _pk_store.name set from storage {ns}:temp _pk_iter[0].name
execute if data storage {ns}:temp _pk_store{{name:""}} run data remove storage {ns}:temp _pk_store.name
function {ns}:v{version}/zombies/perks/store_data with storage {ns}:temp _pk_store
execute if data storage {ns}:temp _pk_store.name run function {ns}:v{version}/zombies/perks/store_data_name with storage {ns}:temp _pk_store

# Shared random-perk pool (power-up and Der Wunderfizz).
function {ns}:v{version}/zombies/perks/pool/mark with storage {ns}:temp _pk_store

execute as @n[tag={ns}.pk_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/perks/on_right_click",executor:"source"}}
execute as @n[tag={ns}.pk_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/perks/on_hover",executor:"source"}}

# Potion by default; maps can override display_item and item_model.
data modify storage {ns}:temp _pk_disp.tag set value "{ns}.pk_display"
data modify storage {ns}:temp _pk_disp.item_id set value ""
data modify storage {ns}:temp _pk_disp.item_model set value ""
data modify storage {ns}:temp _pk_disp.yaw set value 0.0
execute if data storage {ns}:temp _pk_iter[0].display_item run data modify storage {ns}:temp _pk_disp.item_id set from storage {ns}:temp _pk_iter[0].display_item
execute if data storage {ns}:temp _pk_iter[0].item_model run data modify storage {ns}:temp _pk_disp.item_model set from storage {ns}:temp _pk_iter[0].item_model
execute if data storage {ns}:temp _pk_disp{{item_id:""}} run data modify storage {ns}:temp _pk_disp.item_id set value "minecraft:potion"
execute if data storage {ns}:temp _pk_disp{{item_model:""}} run data modify storage {ns}:temp _pk_disp.item_model set value "minecraft:potion"

# Per-perk default machine models when the map set none. Other perks need a child model overriding accent and accent2
# (see perk_machine_juggernog.json) and a line here.
data modify storage {ns}:temp _pk_disp.perk_id set from storage {ns}:temp _pk_iter[0].perk_id
execute if data storage {ns}:temp _pk_disp{{item_model:"minecraft:potion"}} run function {ns}:v{version}/zombies/perks/override_perk_model with storage {ns}:temp _pk_disp
execute if data storage {ns}:temp _pk_iter[0].rotation[0] run data modify storage {ns}:temp _pk_disp.yaw set from storage {ns}:temp _pk_iter[0].rotation[0]
execute as @n[tag={ns}.pk_new] at @s align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _pk_disp
execute as @n[tag={ns}.pk_new] at @s run tp @s ~ ~2 ~
tag @n[tag={ns}.pk_new] add {ns}.perk_machine
tag @n[tag={ns}.pk_new] remove {ns}.pk_new

data remove storage {ns}:temp _pk_iter[0]
execute if data storage {ns}:temp _pk_iter[0] run function {ns}:v{version}/zombies/perks/setup_iter
""")
	write_versioned_function("zombies/perks/override_perk_model", f"""
$data modify storage {ns}:temp _pk_disp.item_model set value "{ns}:perk_machine_$(perk_id)"
""")

	write_versioned_function("zombies/perks/place_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.2f,height:-2.0f,response:true,Rotation:$(rotation),Tags:["{ns}.perk_machine","{ns}.gm_entity","bs.entity.interaction","{ns}.pk_new"]}}
""")

	write_versioned_function("zombies/perks/store_data", f"""
$data modify storage {ns}:zombies perk_data."$(id)" set value {{perk_id:"$(perk_id)"}}
""")

	## Only called when the map set a non-empty name.
	write_versioned_function("zombies/perks/store_data_name", f"""
$data modify storage {ns}:zombies perk_data."$(id)".name set value "$(name)"
""")

