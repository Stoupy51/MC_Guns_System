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

	# Chip-in progress is per-player, so it mirrors the ownership objectives and clears with them
	perkpaid_objectives_add: str = "\n".join(
		f"scoreboard objectives add {ns}.zb.perkpaid.{perk_id} dummy"
		for perk_id in PERK_DEFINITIONS
	)

	## Perk machine entity scoreboards
	write_load_file(f"""
# Perk machine entity scoreboards
scoreboard objectives add {ns}.zb.perk.id dummy
scoreboard objectives add {ns}.zb.perk.price dummy
# Map-defined price, kept so dynamic discounts (solo Quick Revive) can be reverted
scoreboard objectives add {ns}.zb.perk.base_price dummy
scoreboard objectives add {ns}.zb.perk.power dummy
# Chip-in chunk size (0 = disabled, buy in one payment)
scoreboard objectives add {ns}.zb.perk.partial dummy

# Perk ownership scoreboards
{perk_objectives_add}

# Per-player chip-in progress
{perkpaid_objectives_add}
""")

	## Signal function tag for extensibility
	write_tag("zombies/on_new_perk", Mem.ctx.data[ns].function_tags, [])

	## Setup: iterate perk compounds, summon interaction entities
	write_versioned_function("zombies/perks/setup", f"""
scoreboard players set #pk_counter {ns}.data 0
data modify storage {ns}:zombies perk_data set value {{}}
data modify storage {ns}:temp _pk_iter set from storage {ns}:zombies game.map.perks
execute if data storage {ns}:temp _pk_iter[0] run function {ns}:v{version}/zombies/perks/setup_iter
""")

	# When the map leaves price at -1 (auto), resolve the recommended price from the perk_id.
	price_resolve_lines: str = "\n".join(
		f'execute if score @n[tag={ns}.pk_new] {ns}.zb.perk.price matches -1 if data storage {ns}:temp _pk_price{{perk_id:"{perk_id}"}} run scoreboard players set @n[tag={ns}.pk_new] {ns}.zb.perk.price {RECOMMENDED_PRICES.get(perk_id, 2000)}'  # noqa: E501
		for perk_id in PERK_DEFINITIONS
	)
	write_versioned_function("zombies/perks/setup_iter", f"""
# Assign incrementing ID
scoreboard players add #pk_counter {ns}.data 1

# Read relative position and convert to absolute
execute store result score #pkx {ns}.data run data get storage {ns}:temp _pk_iter[0].pos[0]
execute store result score #pky {ns}.data run data get storage {ns}:temp _pk_iter[0].pos[1]
execute store result score #pkz {ns}.data run data get storage {ns}:temp _pk_iter[0].pos[2]
scoreboard players operation #pkx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #pky {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #pkz {ns}.data += #gm_base_z {ns}.data

# Store absolute position and rotation for macro
execute store result storage {ns}:temp _pk.x int 1 run scoreboard players get #pkx {ns}.data
execute store result storage {ns}:temp _pk.y int 1 run scoreboard players get #pky {ns}.data
execute store result storage {ns}:temp _pk.z int 1 run scoreboard players get #pkz {ns}.data
data modify storage {ns}:temp _pk.rotation set from storage {ns}:temp _pk_iter[0].rotation

# Summon interaction entity
function {ns}:v{version}/zombies/perks/place_at with storage {ns}:temp _pk

# Set scoreboards on entity
scoreboard players operation @n[tag={ns}.pk_new] {ns}.zb.perk.id = #pk_counter {ns}.data
execute store result score @n[tag={ns}.pk_new] {ns}.zb.perk.price run data get storage {ns}:temp _pk_iter[0].price
# price -1 = auto: resolve the recommended price for this machine's perk_id (compound match needs a
# flat key: [0]{{...}} after an index is invalid NBT path syntax)
data modify storage {ns}:temp _pk_price.perk_id set from storage {ns}:temp _pk_iter[0].perk_id
{price_resolve_lines}
# Remember the map-defined price so solo Quick Revive can be reverted when players join
scoreboard players operation @n[tag={ns}.pk_new] {ns}.zb.perk.base_price = @n[tag={ns}.pk_new] {ns}.zb.perk.price
# Tag Quick Revive machines for dynamic solo pricing (copy [0] to a flat key: [0]{{...}} is invalid path syntax)
data modify storage {ns}:temp _pk_qr.perk_id set from storage {ns}:temp _pk_iter[0].perk_id
execute if data storage {ns}:temp _pk_qr{{perk_id:"quick_revive"}} run tag @n[tag={ns}.pk_new] add {ns}.pk_quick_revive
# Store power requirement as 1/0 (true stored as 1b in NBT, data get returns 1)
execute store result score @n[tag={ns}.pk_new] {ns}.zb.perk.power run data get storage {ns}:temp _pk_iter[0].power
# Chip-in chunk (absent on maps saved before the field existed -> the failed read stores 0 = disabled)
execute store result score @n[tag={ns}.pk_new] {ns}.zb.perk.partial run data get storage {ns}:temp _pk_iter[0].partial_price

# Store perk_id in indexed storage for later lookup
execute store result storage {ns}:temp _pk_store.id int 1 run scoreboard players get #pk_counter {ns}.data
data modify storage {ns}:temp _pk_store.perk_id set from storage {ns}:temp _pk_iter[0].perk_id
# Optional custom label: kept only when the map set a non-empty name; otherwise left absent so the
# hover/label logic falls back to the perk's canonical name (PERK_DEFINITIONS display_name).
data remove storage {ns}:temp _pk_store.name
data modify storage {ns}:temp _pk_store.name set from storage {ns}:temp _pk_iter[0].name
execute if data storage {ns}:temp _pk_store{{name:""}} run data remove storage {ns}:temp _pk_store.name
function {ns}:v{version}/zombies/perks/store_data with storage {ns}:temp _pk_store
execute if data storage {ns}:temp _pk_store.name run function {ns}:v{version}/zombies/perks/store_data_name with storage {ns}:temp _pk_store

# Mark this perk as present on the map (shared random-perk pool: power-up + Der Wunderfizz)
function {ns}:v{version}/zombies/perks/pool/mark with storage {ns}:temp _pk_store

# Register Bookshelf events
execute as @n[tag={ns}.pk_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/perks/on_right_click",executor:"source"}}
execute as @n[tag={ns}.pk_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/perks/on_hover",executor:"source"}}

# Spawn visual item_display at machine position (default: potion; overridable via display_item + item_model map fields)
data modify storage {ns}:temp _pk_disp.tag set value "{ns}.pk_display"
data modify storage {ns}:temp _pk_disp.item_id set value ""
data modify storage {ns}:temp _pk_disp.item_model set value ""
data modify storage {ns}:temp _pk_disp.yaw set value 0.0
execute if data storage {ns}:temp _pk_iter[0].display_item run data modify storage {ns}:temp _pk_disp.item_id set from storage {ns}:temp _pk_iter[0].display_item
execute if data storage {ns}:temp _pk_iter[0].item_model run data modify storage {ns}:temp _pk_disp.item_model set from storage {ns}:temp _pk_iter[0].item_model
execute if data storage {ns}:temp _pk_disp{{item_id:""}} run data modify storage {ns}:temp _pk_disp.item_id set value "minecraft:potion"
execute if data storage {ns}:temp _pk_disp{{item_model:""}} run data modify storage {ns}:temp _pk_disp.item_model set value "minecraft:potion"

# Per-perk default machine models (only when the map didn't set a custom model)
# Copy perk_id to a named key first ([0]{{...}} compound match after an index is invalid NBT path syntax)
# Other perks: add a child model overriding accent/accent2 (see perk_machine_juggernog.json) and a line here
data modify storage {ns}:temp _pk_disp.perk_id set from storage {ns}:temp _pk_iter[0].perk_id
execute if data storage {ns}:temp _pk_disp{{item_model:"minecraft:potion"}} run function {ns}:v{version}/zombies/perks/override_perk_model with storage {ns}:temp _pk_disp
execute if data storage {ns}:temp _pk_iter[0].rotation[0] run data modify storage {ns}:temp _pk_disp.yaw set from storage {ns}:temp _pk_iter[0].rotation[0]
execute as @n[tag={ns}.pk_new] at @s align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _pk_disp
execute as @n[tag={ns}.pk_new] at @s run tp @s ~ ~2 ~
tag @n[tag={ns}.pk_new] add {ns}.perk_machine
tag @n[tag={ns}.pk_new] remove {ns}.pk_new

# Iterate next
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

	## Attach the optional custom label (only called when the map set a non-empty name)
	write_versioned_function("zombies/perks/store_data_name", f"""
$data modify storage {ns}:zombies perk_data."$(id)".name set value "$(name)"
""")

