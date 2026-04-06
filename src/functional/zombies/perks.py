
# Perk Machine System
# Stationary machines where players buy gameplay-enhancing perks.
# Available perks and their behavior are defined in PERK_DEFINITIONS.
from stewbeet import Mem, write_load_file, write_tag, write_versioned_function

from ..helpers import MGS_TAG
from .common import deny_not_enough_points_body, deny_requires_power_body, game_active_guard_cmd

PERK_DEFINITIONS: dict[str, dict[str, str | list[str]]] = {
	"juggernog": {
		"display_name": "Juggernog",
		"message": "🍺 Juggernog! Max HP: 40",
		"message_color": "dark_red",
		"commands": [
			"attribute @s minecraft:max_health base set 40",
		],
	},
	"speed_cola": {
		"display_name": "Speed Cola",
		"message": "⚡ Speed Cola! Faster reload",
		"message_color": "green",
		"commands": [
			"scoreboard players set @s {ns}.special.quick_reload 50",
		],
	},
	"double_tap": {
		"display_name": "Double Tap",
		"message": "🔥 Double Tap! More damage",
		"message_color": "gold",
		"commands": [
			"scoreboard players set @s {ns}.special.additional_shots 1",
		],
	},
	"quick_revive": {
		"display_name": "Quick Revive",
		"message": "💚 Quick Revive! You can revive teammates",
		"message_color": "aqua",
	},
	"mule_kick": {
		"display_name": "Mule Kick",
		"message": "🎒 Mule Kick! Third weapon slot unlocked",
		"message_color": "gold",
	},
}


def generate_perks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	perk_objectives_add: str = "\n".join(
		f"scoreboard objectives add {ns}.zb.perk.{perk_id} dummy"
		for perk_id in PERK_DEFINITIONS
	)
	perk_reset_all_players: str = "\n".join(
		f"scoreboard players reset * {ns}.zb.perk.{perk_id}"
		for perk_id in PERK_DEFINITIONS
	)

	## Perk machine entity scoreboards
	write_load_file(f"""
# Perk machine entity scoreboards
scoreboard objectives add {ns}.zb.perk.id dummy
scoreboard objectives add {ns}.zb.perk.price dummy
scoreboard objectives add {ns}.zb.perk.power dummy

# Perk ownership scoreboards
{perk_objectives_add}
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
# Store power requirement as 1/0 (true stored as 1b in NBT, data get returns 1)
execute store result score @n[tag={ns}.pk_new] {ns}.zb.perk.power run data get storage {ns}:temp _pk_iter[0].power

# Store perk_id in indexed storage for later lookup
execute store result storage {ns}:temp _pk_store.id int 1 run scoreboard players get #pk_counter {ns}.data
data modify storage {ns}:temp _pk_store.perk_id set from storage {ns}:temp _pk_iter[0].perk_id
data modify storage {ns}:temp _pk_store.name set from storage {ns}:temp _pk_iter[0].perk_id
execute if data storage {ns}:temp _pk_iter[0].name run data modify storage {ns}:temp _pk_store.name set from storage {ns}:temp _pk_iter[0].name
function {ns}:v{version}/zombies/perks/store_data with storage {ns}:temp _pk_store

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
execute if data storage {ns}:temp _pk_iter[0].rotation[0] run data modify storage {ns}:temp _pk_disp.yaw set from storage {ns}:temp _pk_iter[0].rotation[0]
execute as @n[tag={ns}.pk_new] at @s run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _pk_disp
tag @n[tag={ns}.pk_new] add {ns}.perk_machine
tag @n[tag={ns}.pk_new] remove {ns}.pk_new

# Iterate next
data remove storage {ns}:temp _pk_iter[0]
execute if data storage {ns}:temp _pk_iter[0] run function {ns}:v{version}/zombies/perks/setup_iter
""")

	write_versioned_function("zombies/perks/place_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.0f,height:2.0f,response:true,Rotation:$(rotation),Tags:["{ns}.perk_machine","{ns}.gm_entity","bs.entity.interaction","{ns}.pk_new"]}}
""")

	write_versioned_function("zombies/perks/store_data", f"""
$data modify storage {ns}:zombies perk_data."$(id)" set value {{perk_id:"$(perk_id)",name:"$(name)"}}
""")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/perks/on_right_click", f"""
# Guard: game must be active
{game_active_guard_cmd(ns)}

# Check power requirement
execute store result score #pk_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.power
execute if score #pk_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 run return run function {ns}:v{version}/zombies/perks/deny_requires_power

# Look up perk_id
execute store result storage {ns}:temp _pk_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.id
function {ns}:v{version}/zombies/perks/lookup_perk with storage {ns}:temp _pk_buy

# Check if player already has this perk
function {ns}:v{version}/zombies/perks/check_owned with storage {ns}:temp _pk_data
execute if score #pk_owned {ns}.data matches 1 run return run function {ns}:v{version}/zombies/perks/deny_already_owned

# Get price and check points
execute store result score #pk_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.price
execute unless score @s {ns}.zb.points >= #pk_price {ns}.data run return run function {ns}:v{version}/zombies/perks/deny_not_enough_points

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #pk_price {ns}.data

# Apply perk effect (sets scoreboard + calls specific perk function)
function {ns}:v{version}/zombies/perks/apply with storage {ns}:temp _pk_data

# Signal
function #{ns}:zombies/on_new_perk

# Sound
function {ns}:v{version}/zombies/feedback/sound_success
""")

	write_versioned_function("zombies/perks/deny_requires_power", f"""
{deny_requires_power_body(ns, version, "perk machine")}
""")

	write_versioned_function("zombies/perks/deny_already_owned", f"""
tellraw @s [{MGS_TAG},{{"text":"You already own this perk.","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/perks/deny_not_enough_points", f"""
{deny_not_enough_points_body(ns, version, "#pk_price")}
""")

	write_versioned_function("zombies/perks/lookup_perk", f"""
$data modify storage {ns}:temp _pk_data set from storage {ns}:zombies perk_data."$(id)"
""")

	hover_name_lines: str = "\n".join(
		f'execute unless data storage {ns}:temp _pk_data.name if data storage {ns}:temp _pk_data{{perk_id:"{perk_id}"}} run data modify storage {ns}:temp _pk_hover_name set value "{perk_data["display_name"]}"'  # noqa: E501
		for perk_id, perk_data in PERK_DEFINITIONS.items()
	)
	write_versioned_function("zombies/perks/get_hover_name", f"""
data modify storage {ns}:temp _pk_hover_name set value "Perk"
execute if data storage {ns}:temp _pk_data.name run data modify storage {ns}:temp _pk_hover_name set from storage {ns}:temp _pk_data.name
{hover_name_lines}
""")

	write_versioned_function("zombies/perks/check_owned", f"""
scoreboard players set #pk_owned {ns}.data 0
$execute if score @s {ns}.zb.perk.$(perk_id) matches 1 run scoreboard players set #pk_owned {ns}.data 1
""")

	write_versioned_function("zombies/perks/apply", f"""
# Set perk scoreboard for the player
$scoreboard players set @s {ns}.zb.perk.$(perk_id) 1

# Call perk-specific effect function
$function {ns}:v{version}/zombies/perks/apply/$(perk_id)
""")

	## Per-perk effect functions (generated from top-level metadata)
	for perk_id, perk_data in PERK_DEFINITIONS.items():
		extra_commands: str = "\n".join(
			command.replace("{ns}", ns)
			for command in perk_data.get("commands", [])
		)
		write_versioned_function(f"zombies/perks/apply/{perk_id}", f"""
{extra_commands}
tellraw @s [{MGS_TAG},{{"text":"{perk_data["message"]}","color":"{perk_data["message_color"]}"}}]
""")

	## Hover events (executor: "source" = player)
	write_versioned_function("zombies/perks/on_hover", f"""
execute store result score #pk_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.price
execute store result storage {ns}:temp _pk_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.id
function {ns}:v{version}/zombies/perks/lookup_perk with storage {ns}:temp _pk_hover
function {ns}:v{version}/zombies/perks/get_hover_name
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🥤 ","color":"dark_purple"}},{{"storage":"{ns}:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true}},{{"text":" - Cost: ","color":"gray"}},{{"score":{{"name":"#pk_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}],priority:'notification',freeze:5}}
function #smithed.actionbar:message
""")  # noqa: E501

	## Hook into game start: reset perk scoreboards
	write_versioned_function("zombies/start", f"""
# Reset perk scoreboards for all known score holders (including offline players).
{perk_reset_all_players}
""")

	## Hook into preload_complete: setup perk machines
	write_versioned_function("zombies/preload_complete", f"""
# Setup perk machines
execute if data storage {ns}:zombies game.map.perks[0] run function {ns}:v{version}/zombies/perks/setup
""")

	## Hook into stop: remove perk effects
	write_versioned_function("zombies/stop", f"""
# Reset perk effects
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:max_health base set 20
tag @a remove {ns}.perk.speed_cola
tag @a remove {ns}.perk.double_tap
tag @a remove {ns}.perk.quick_revive

# Reset special scoreboards granted by perks
scoreboard players set @a {ns}.special.quick_reload 0
scoreboard players set @a {ns}.special.additional_shots 0
scoreboard players set @a {ns}.special.instant_kill 0
scoreboard players set @a {ns}.special.infinite_ammo 0
scoreboard players set @a {ns}.special.quick_swap 0

# Reset perk scoreboards for all known score holders (including offline players).
{perk_reset_all_players}
""")
