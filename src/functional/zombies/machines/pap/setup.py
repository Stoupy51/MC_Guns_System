""" Machine scoreboards, the scope and camo tables, placing each machine and its hover. """
# ruff: noqa: E501
# Imports
from stewbeet import ItemModifier, JsonDict, Mem, set_json_encoder, write_load_file, write_versioned_function

from .....config.catalogs import SCOPE_VARIANTS
from .....database.camo import MATERIALS


# Functions
def write_pap_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Item modifier: copy upgraded stats from temp storage back into selected gun item.
	pap_stats_modifier: JsonDict = {
		"function": "minecraft:copy_custom_data",
		"source": {"type": "minecraft:storage", "source": f"{ns}:temp"},
		"ops": [
			{"source": "_pap_extract.stats", "target": f"{ns}.stats", "op": "replace"},
			{"source": "_pap_extract.weapon", "target": f"{ns}.weapon", "op": "replace"},
		],
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/zb_pap_apply_stats"] = set_json_encoder(ItemModifier(pap_stats_modifier), max_level=-1)

	# Entity scoreboards for PAP machines.
	write_load_file(f"""
# Pack-a-Punch machine scoreboards
scoreboard objectives add {ns}.zb.pap.id dummy
scoreboard objectives add {ns}.zb.pap.price dummy
scoreboard objectives add {ns}.zb.pap.power dummy
scoreboard objectives add {ns}.pap_anim dummy
# 1 when the player who started this PAP owns Timeslip (animation runs 3x faster)
scoreboard objectives add {ns}.zb.pap.timeslip dummy

# Per-player PAP tracking (for cleanup when weapon is lost/collected)
scoreboard objectives add {ns}.zb.pap_s dummy
scoreboard objectives add {ns}.zb.pap_mid dummy
""")

	# Load scope variant data for PAP randomization
	scope_data_lines: list[str] = []
	for base_weapon, suffixes in SCOPE_VARIANTS.items():
		entries: list[str] = []
		for suffix in suffixes:
			weapon_id = f"{base_weapon}{suffix}"
			entry = f'{{id:"{weapon_id}",model:"{ns}:{weapon_id}",zoom:"{ns}:{weapon_id}_zoom"'
			if suffix == "_3":
				entry += ",scope_level:3"
			elif suffix == "_4":
				entry += ",scope_level:4"
			entry += "}"
			entries.append(entry)
		scope_data_lines.append(
			f'data modify storage {ns}:zombies scope_variants."{base_weapon}" set value [{",".join(entries)}]'
		)
	write_load_file("\n".join(scope_data_lines))

	# Load camo variant data for PAP randomization
	all_camos = list(MATERIALS.keys())
	all_camos_str = ",".join(f'"{c}"' for c in all_camos)
	camo_data_lines: list[str] = [f'data modify storage {ns}:zombies camo_variants._default set value [{all_camos_str}]']
	write_load_file("\n".join(camo_data_lines))

	# Setup: iterate map compounds and summon interaction entities.
	write_versioned_function("zombies/pap/setup", f"""
scoreboard players set #pap_counter {ns}.data 0
data modify storage {ns}:zombies pap_data set value {{}}
data modify storage {ns}:temp _pap_iter set from storage {ns}:zombies game.map.pap_machines
execute if data storage {ns}:temp _pap_iter[0] run function {ns}:v{version}/zombies/pap/setup_iter
""")

	write_versioned_function("zombies/pap/setup_iter", f"""
# Assign incrementing machine id
scoreboard players add #pap_counter {ns}.data 1

# Convert relative map coords to absolute world coords
execute store result score #papx {ns}.data run data get storage {ns}:temp _pap_iter[0].pos[0]
execute store result score #papy {ns}.data run data get storage {ns}:temp _pap_iter[0].pos[1]
execute store result score #papz {ns}.data run data get storage {ns}:temp _pap_iter[0].pos[2]
scoreboard players operation #papx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #papy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #papz {ns}.data += #gm_base_z {ns}.data

# Store absolute coords and rotation for summon macro
execute store result storage {ns}:temp _pap_place.x int 1 run scoreboard players get #papx {ns}.data
execute store result storage {ns}:temp _pap_place.y int 1 run scoreboard players get #papy {ns}.data
execute store result storage {ns}:temp _pap_place.z int 1 run scoreboard players get #papz {ns}.data
data modify storage {ns}:temp _pap_place.rotation set from storage {ns}:temp _pap_iter[0].rotation

# Summon interaction entity
function {ns}:v{version}/zombies/pap/place_at with storage {ns}:temp _pap_place

# Set machine metadata
scoreboard players operation @n[tag={ns}.pap_new] {ns}.zb.pap.id = #pap_counter {ns}.data
execute store result score @n[tag={ns}.pap_new] {ns}.zb.pap.price run data get storage {ns}:temp _pap_iter[0].price
execute store result score @n[tag={ns}.pap_new] {ns}.zb.pap.power run data get storage {ns}:temp _pap_iter[0].power

# Register Bookshelf interaction callbacks
execute as @n[tag={ns}.pap_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/pap/on_right_click",executor:"source"}}
execute as @n[tag={ns}.pap_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/pap/on_hover",executor:"source"}}

# Initialize animation state: -1 = idle
scoreboard players set @n[tag={ns}.pap_new] {ns}.pap_anim -1

# Spawn visual item_display at machine position (default: netherite_block; overridable via display_item + item_model map fields)
data modify storage {ns}:temp _pap_disp.tag set value "{ns}.pap_display"
data modify storage {ns}:temp _pap_disp.item_id set value ""
data modify storage {ns}:temp _pap_disp.item_model set value ""
data modify storage {ns}:temp _pap_disp.yaw set value 0.0
execute if data storage {ns}:temp _pap_iter[0].display_item run data modify storage {ns}:temp _pap_disp.item_id set from storage {ns}:temp _pap_iter[0].display_item
execute if data storage {ns}:temp _pap_iter[0].item_model run data modify storage {ns}:temp _pap_disp.item_model set from storage {ns}:temp _pap_iter[0].item_model
execute if data storage {ns}:temp _pap_disp{{item_id:""}} run data modify storage {ns}:temp _pap_disp.item_id set value "minecraft:netherite_block"
execute if data storage {ns}:temp _pap_disp{{item_model:""}} run data modify storage {ns}:temp _pap_disp.item_model set value "{ns}:pack_a_punch"
execute if data storage {ns}:temp _pap_iter[0].rotation[0] run data modify storage {ns}:temp _pap_disp.yaw set from storage {ns}:temp _pap_iter[0].rotation[0]
execute as @n[tag={ns}.pap_new] at @s positioned ^ ^ ^-0.49 positioned ~ ~-0.4 ~ run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _pap_disp
execute as @n[tag={ns}.pap_new] at @s run tp @s ~ ~2 ~

# Store display metadata for lookup (reuse the computed _pap_disp fields)
execute store result storage {ns}:temp _pap_store.id int 1 run scoreboard players get #pap_counter {ns}.data
data modify storage {ns}:temp _pap_store.name set value "Pack-a-Punch"
execute if data storage {ns}:temp _pap_iter[0].name run data modify storage {ns}:temp _pap_store.name set from storage {ns}:temp _pap_iter[0].name
data modify storage {ns}:temp _pap_store.display_tag set from storage {ns}:temp _pap_disp.tag
data modify storage {ns}:temp _pap_store.display_item_id set from storage {ns}:temp _pap_disp.item_id
data modify storage {ns}:temp _pap_store.display_item_model set from storage {ns}:temp _pap_disp.item_model
data modify storage {ns}:temp _pap_store.display_yaw set from storage {ns}:temp _pap_disp.yaw
function {ns}:v{version}/zombies/pap/store_data with storage {ns}:temp _pap_store

tag @n[tag={ns}.pap_new] remove {ns}.pap_new

# Continue iteration
data remove storage {ns}:temp _pap_iter[0]
execute if data storage {ns}:temp _pap_iter[0] run function {ns}:v{version}/zombies/pap/setup_iter
""")

	write_versioned_function("zombies/pap/place_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.69f,height:-2.0f,response:true,Rotation:$(rotation),Tags:["{ns}.pap_machine","{ns}.gm_entity","bs.entity.interaction","{ns}.pap_new"]}}
""")

	write_versioned_function("zombies/pap/store_data", f"""
$data modify storage {ns}:zombies pap_data."$(id)" set value {{name:"$(name)",display_tag:"$(display_tag)",display_item_id:"$(display_item_id)",display_item_model:"$(display_item_model)",display_yaw:$(display_yaw)}}
""")

	write_versioned_function("zombies/pap/lookup_machine", f"""
$data modify storage {ns}:temp _pap_machine set from storage {ns}:zombies pap_data."$(id)"
""")

	write_versioned_function("zombies/pap/on_hover", f"""
execute store result score #pap_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.price
# Bonfire Sale: Pack-a-Punch costs 1000 while active
execute if score #zb_bonfire_sale_timer {ns}.data matches 1.. run scoreboard players set #pap_price {ns}.data 1000
execute store result storage {ns}:temp _pap_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/lookup_machine with storage {ns}:temp _pap_hover
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚙ ","color":"dark_red"}},{{"storage":"{ns}:temp","nbt":"_pap_machine.name","color":"gold","interpret":true}},{{"text":" - Cost: ","color":"gray"}},{{"score":{{"name":"#pap_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}],priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

