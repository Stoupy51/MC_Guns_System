
# Perk Machine System
# Stationary machines where players buy gameplay-enhancing perks.
# Available perks and their behavior are defined in PERK_DEFINITIONS.
from stewbeet import JsonDict, Mem, write_load_file, write_tag, write_versioned_function

from ..helpers import MGS_TAG, reset_special_scores_lines
from ..stamina import STAM_MAX
from .common import deny_not_enough_points_body, deny_requires_power_body, game_active_guard_cmd

# Each perk defines:
# - message/message_color: chat feedback on purchase
# - text_color: text color matching the perk MACHINE model's dye color (others.py override_model),
#   used everywhere the perk is listed (info paper, perk display items) so colors stay consistent
PERK_DEFINITIONS: dict[str, JsonDict] = {
	"juggernog": {
		"display_name": "Juggernog",
		"message": "🍺 Juggernog! Max HP: 40",
		"message_color": "dark_red",
		"text_color": "red",
		"commands": [
			"attribute @s minecraft:max_health base set 40",
		],
		"removal_commands": [
			"attribute @s minecraft:max_health base reset",
		],
	},
	"speed_cola": {
		"display_name": "Speed Cola",
		"message": "⚡ Speed Cola! Faster reload",
		"message_color": "green",
		"text_color": "green",
		"commands": [
			"scoreboard players set @s {ns}.special.quick_reload 50",
		],
		"removal_commands": [
			"scoreboard players set @s {ns}.special.quick_reload 0",
		],
	},
	"double_tap": {
		"display_name": "Double Tap",
		"message": "🔥 Double Tap! More damage",
		"message_color": "gold",
		"text_color": "yellow",
		"commands": [
			"scoreboard players set @s {ns}.special.additional_shots 1",
		],
		"removal_commands": [
			"scoreboard players set @s {ns}.special.additional_shots 0",
		],
	},
	"quick_revive": {
		"display_name": "Quick Revive",
		"message": "💚 Quick Revive! You can revive teammates",
		"message_color": "aqua",
		"text_color": "aqua",
		"commands": [
			"tag @s add {ns}.perk.quick_revive",
		],
		# No removal_commands: tag removal and score management handled by solo_qr_complete
		# persistent_score=True: lose_all does NOT reset this score (solo_qr_complete manages it)
		"persistent_score": True,
	},
	"mule_kick": {
		"display_name": "Mule Kick",
		"message": "🎒 Mule Kick! Third weapon slot unlocked",
		"message_color": "gold",
		"text_color": "dark_green",
	},
	"stamin_up": {
		"display_name": "Stamin-Up",
		"message": "🏃 Stamin-Up! Sprint longer, move faster",
		"message_color": "yellow",
		"text_color": "gold",
		# BO1 Zombies Stamin-Up (see zombies/stamina.md): double sprint endurance + 7% move speed
		# (multiplicative, on top of the weapon/base movement model). The stam bump refills the
		# new headroom instantly so the visible bar doesn't drop at purchase.
		"commands": [
			"attribute @s minecraft:movement_speed modifier add {ns}:stamin_up 0.07 add_multiplied_total",
			f"scoreboard players set @s {{ns}}.stam_bonus {STAM_MAX}",
			f"scoreboard players add @s {{ns}}.stam {STAM_MAX}",
		],
		"removal_commands": [
			"attribute @s minecraft:movement_speed modifier remove {ns}:stamin_up",
			"scoreboard players set @s {ns}.stam_bonus 0",
		],
	},
	"phd_flopper": {
		"display_name": "PhD Flopper",
		"message": "🧪 PhD Flopper! Immune to explosions & fall damage",
		"message_color": "dark_purple",
		"text_color": "dark_purple",
		# Fall damage is nulled by an attribute; explosive self-damage is gated on the special score
		# in the shared explosion paths (weapon/projectile.py, weapon/grenade.py) and trap damage.
		"commands": [
			"attribute @s minecraft:fall_damage_multiplier base set 0",
			"scoreboard players set @s {ns}.special.phd_flopper 1",
		],
		"removal_commands": [
			"attribute @s minecraft:fall_damage_multiplier base reset",
			"scoreboard players set @s {ns}.special.phd_flopper 0",
		],
	},
	"deadshot": {
		"display_name": "Deadshot Daiquiri",
		"message": "🎯 Deadshot Daiquiri! +Accuracy, -Recoil",
		"message_color": "dark_green",
		"text_color": "dark_green",
		# Read in the weapon spread path (raycast.py) and the recoil path (kick.py): both scale to 65%.
		"commands": [
			"scoreboard players set @s {ns}.special.deadshot 1",
		],
		"removal_commands": [
			"scoreboard players set @s {ns}.special.deadshot 0",
		],
	},
	"timeslip": {
		"display_name": "Timeslip",
		"message": "⏳ Timeslip! Faster traps & Mystery Box",
		"message_color": "light_purple",
		"text_color": "light_purple",
		# Owner-only speed-ups keyed off the special score: trap cooldown x0.75 (traps.py) and Mystery
		# Box spin x2 (mystery_box.py). Base factor is x2 (no official BO4 number; "about half the time"
		# ≈ 2x, matching the music_box_short jingle ratio) — EXCEPT Pack-a-Punch, which is x3 because its
		# 300-tick animation is already long.
		# TODO(zombies README task 5): Pack-a-Punch x3 (rescale the 300-tick anim phases + swap the
		# jingle to zombies/pap/jingle_sting_short, the 3x asset already generated) and grenade throw
		# cooldown x0.5 are still pending — both need in-engine timing verification (PAP has many
		# exact-tick phase triggers; the grenade throw-cooldown score the README points at does not exist
		# yet and needs to be located/clarified first).
		"commands": [
			"scoreboard players set @s {ns}.special.timeslip 1",
		],
		"removal_commands": [
			"scoreboard players set @s {ns}.special.timeslip 0",
		],
	},
}


def perk_effects_teardown(ns: str, selector: str) -> str:
	""" Return the lines stripping every effect a zombies perk can leave on a player.

	Run at BOTH ends of a game: at stop to hand players back a clean profile, and at start because
	the effects can also arrive from outside zombies entirely — the multiplayer/missions loadout
	perks and the debug menu write the same `special.*` scores, and nothing else clears them for a
	zombies player. Wiping the whole `SPECIAL_SCORES` set (not just the ones perks grant) is what
	keeps e.g. a multiplayer Quick Reload class from handing out free Speed Cola in zombies.
	"""
	return f"""
execute as {selector} run attribute @s minecraft:max_health base reset
execute as {selector} run attribute @s minecraft:movement_speed modifier remove {ns}:stamin_up
execute as {selector} run attribute @s minecraft:fall_damage_multiplier base reset
scoreboard players set {selector} {ns}.stam_bonus 0
tag {selector} remove {ns}.perk.speed_cola
tag {selector} remove {ns}.perk.double_tap
tag {selector} remove {ns}.perk.quick_revive
{reset_special_scores_lines(ns, selector)}
""".strip()


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
	# Chip-in progress is per-player (nobody pays for someone else's perk), so it mirrors the
	# ownership objectives one-for-one and is cleared at the same points they are.
	perkpaid_objectives_add: str = "\n".join(
		f"scoreboard objectives add {ns}.zb.perkpaid.{perk_id} dummy"
		for perk_id in PERK_DEFINITIONS
	)
	perkpaid_reset_all_players: str = "\n".join(
		f"scoreboard players reset * {ns}.zb.perkpaid.{perk_id}"
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
data modify storage {ns}:temp _pk_store.name set from storage {ns}:temp _pk_iter[0].perk_id
execute if data storage {ns}:temp _pk_iter[0].name run data modify storage {ns}:temp _pk_store.name set from storage {ns}:temp _pk_iter[0].name
function {ns}:v{version}/zombies/perks/store_data with storage {ns}:temp _pk_store

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
$data modify storage {ns}:zombies perk_data."$(id)" set value {{perk_id:"$(perk_id)",name:"$(name)"}}
""")

	## ── Shared "available perk pool" helper ─────────────────────────────────────
	# One source of truth for "which perks can this player still be given", used by BOTH the
	# random-perk power-up (powerups.py) and Der Wunderfizz (zombies README task 4).
	# A perk is available for the target player when:
	#   - the perk has a machine placed on this map (#map_perk_<id> == 1), OR the caller set
	#     #pool_all_perks (Origins-style "roll across every perk"), AND
	#   - the target player (tagged {ns}.pool_target) does not already own it.
	# `mark` is called once per placed machine during setup; the flags are cleared at game start.
	perk_ids: list[str] = list(PERK_DEFINITIONS.keys())
	num_perks: int = len(perk_ids)

	def pool_avail_block(perk_id: str) -> str:
		""" Set #pool_slot to 1 iff `perk_id` is available for @n[tag=pool_target], else 0. """
		return (
			f"scoreboard players set #pool_slot {ns}.data 0\n"
			f"execute if score #map_perk_{perk_id} {ns}.data matches 1 run scoreboard players set #pool_slot {ns}.data 1\n"
			f"execute if score #pool_all_perks {ns}.data matches 1 run scoreboard players set #pool_slot {ns}.data 1\n"
			f"execute if score @n[tag={ns}.pool_target] {ns}.zb.perk.{perk_id} matches 1 run scoreboard players set #pool_slot {ns}.data 0"
		)

	## Mark a placed perk as present on the map (macro: perk_id)
	write_versioned_function("zombies/perks/pool/mark", f"""
$scoreboard players set #map_perk_$(perk_id) {ns}.data 1
""")

	## Count available perks into #pool_avail (target = @n[tag={ns}.pool_target], mode = #pool_all_perks)
	count_lines: str = "\n".join(
		f"{pool_avail_block(perk_id)}\nscoreboard players operation #pool_avail {ns}.data += #pool_slot {ns}.data"
		for perk_id in perk_ids
	)
	write_versioned_function("zombies/perks/pool/count", f"""
scoreboard players set #pool_avail {ns}.data 0
{count_lines}
""")

	## Pick one random available perk. Output: #pool_chosen (0..n-1 index, or -1 if none) and
	## storage {ns}:temp _pool.perk_id (only set on success). Caller tags the target + sets #pool_all_perks.
	write_versioned_function("zombies/perks/pool/choose", f"""
function {ns}:v{version}/zombies/perks/pool/count
scoreboard players set #pool_chosen {ns}.data -1
data modify storage {ns}:temp _pool set value {{}}
execute if score #pool_avail {ns}.data matches ..0 run return 0

# Random start index, then walk the list until an available perk is found
execute store result score #pool_roll {ns}.data run random value 0..{num_perks - 1}
scoreboard players set #pool_tries {ns}.data 0
function {ns}:v{version}/zombies/perks/pool/choose_iter
""")

	iter_lines: str = ""
	for i, perk_id in enumerate(perk_ids):
		iter_lines += f"execute if score #pool_roll {ns}.data matches {i} run function {ns}:v{version}/zombies/perks/pool/try_index/{perk_id}\n"
		iter_lines += f"execute if score #pool_chosen {ns}.data matches 0.. run return 0\n"
	write_versioned_function("zombies/perks/pool/choose_iter", f"""
# Safety counter: at most one full loop over the perk list
scoreboard players add #pool_tries {ns}.data 1
execute if score #pool_tries {ns}.data matches {num_perks + 1}.. run return 0
execute if score #pool_chosen {ns}.data matches 0.. run return 0

{iter_lines}
# Nothing available at this index: advance and recurse
scoreboard players add #pool_roll {ns}.data 1
execute if score #pool_roll {ns}.data matches {num_perks}.. run scoreboard players set #pool_roll {ns}.data 0
function {ns}:v{version}/zombies/perks/pool/choose_iter
""")

	for i, perk_id in enumerate(perk_ids):
		write_versioned_function(f"zombies/perks/pool/try_index/{perk_id}", f"""
{pool_avail_block(perk_id)}
execute if score #pool_slot {ns}.data matches 1 run scoreboard players set #pool_chosen {ns}.data {i}
execute if score #pool_slot {ns}.data matches 1 run data modify storage {ns}:temp _pool.perk_id set value "{perk_id}"
""")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/perks/on_right_click", f"""
# Guard: game must be active
{game_active_guard_cmd(ns)}

# Check power requirement. Quick Revive is exempt while solo (Black Ops rule).
execute store result score #pk_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.power
execute store result score #qr_solo {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
execute if score #pk_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 unless entity @n[tag=bs.interaction.target,tag={ns}.pk_quick_revive] run return run function {ns}:v{version}/zombies/perks/deny_requires_power
execute if score #pk_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 if entity @n[tag=bs.interaction.target,tag={ns}.pk_quick_revive] if score #qr_solo {ns}.data matches 2.. run return run function {ns}:v{version}/zombies/perks/deny_requires_power

# Look up perk_id
execute store result storage {ns}:temp _pk_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.id
function {ns}:v{version}/zombies/perks/lookup_perk with storage {ns}:temp _pk_buy

# Check if player already has this perk
function {ns}:v{version}/zombies/perks/check_owned with storage {ns}:temp _pk_data
execute if score #pk_owned {ns}.data matches 1 run return run function {ns}:v{version}/zombies/perks/deny_already_owned

# Get price and check points (chip-in machines charge one chunk per click)
function {ns}:v{version}/zombies/perks/read_price with storage {ns}:temp _pk_data
execute unless score @s {ns}.zb.points >= #pk_price {ns}.data run return run function {ns}:v{version}/zombies/perks/deny_not_enough_points

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #pk_price {ns}.data

# Chip-in: progress is LOCAL, each player pays down their own perk. Stop here unless this
# payment was the one that completed it.
scoreboard players operation #pk_paid {ns}.data += #pk_price {ns}.data
execute if score #pk_partial {ns}.data matches 1.. run function {ns}:v{version}/zombies/perks/store_progress with storage {ns}:temp _pk_data
execute if score #pk_partial {ns}.data matches 1.. if score #pk_paid {ns}.data < #pk_total {ns}.data run return run function {ns}:v{version}/zombies/perks/announce_progress

# Apply perk effect (sets scoreboard + calls specific perk function)
function {ns}:v{version}/zombies/perks/apply with storage {ns}:temp _pk_data

# Signal
function #{ns}:zombies/on_new_perk

# Sound
function {ns}:v{version}/zombies/feedback/sound_success
""")  # noqa: E501

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

	## Price of the next click on the hovered/clicked machine (macro: $(perk_id) selects the
	## player's chip-in progress). #pk_total = full price, #pk_price = what THIS click costs
	## (one chunk when chip-in is on, the last chunk being whatever is left), #pk_paid = progress.
	write_versioned_function("zombies/perks/read_price", f"""
execute store result score #pk_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.price
execute store result score #pk_partial {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.partial
$execute store result score #pk_paid {ns}.data run scoreboard players get @s {ns}.zb.perkpaid.$(perk_id)
scoreboard players operation #pk_total {ns}.data = #pk_price {ns}.data

# Remaining, clamped at 0: solo Quick Revive rewrites the price live, so it can drop below the
# progress already paid. Clamping makes that last click free instead of refunding points.
scoreboard players operation #pk_left {ns}.data = #pk_total {ns}.data
scoreboard players operation #pk_left {ns}.data -= #pk_paid {ns}.data
execute if score #pk_left {ns}.data matches ..0 run scoreboard players set #pk_left {ns}.data 0

# Fixed chunks, last one is the remainder
execute if score #pk_partial {ns}.data matches 1.. run scoreboard players operation #pk_price {ns}.data = #pk_partial {ns}.data
execute if score #pk_partial {ns}.data matches 1.. run scoreboard players operation #pk_price {ns}.data < #pk_left {ns}.data
""")

	write_versioned_function("zombies/perks/store_progress", f"""
$scoreboard players operation @s {ns}.zb.perkpaid.$(perk_id) = #pk_paid {ns}.data
""")

	## Chip-in payment that didn't finish the perk (@s = paying player, _pk_data = the machine's perk)
	write_versioned_function("zombies/perks/announce_progress", f"""
function {ns}:v{version}/zombies/perks/get_hover_name
tellraw @s [{MGS_TAG},{{"text":"🥤 ","color":"dark_purple"}},{{"storage":"{ns}:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true}},{{"text":": ","color":"gray"}},{{"score":{{"name":"#pk_paid","objective":"{ns}.data"}},"color":"green"}},{{"text":"/","color":"gray"}},{{"score":{{"name":"#pk_total","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points paid","color":"gray"}}]
function {ns}:v{version}/zombies/feedback/sound_refill
""")  # noqa: E501

	write_versioned_function("zombies/perks/apply", f"""
# Set perk scoreboard for the player
$scoreboard players set @s {ns}.zb.perk.$(perk_id) 1

# Owning the perk voids any chip-in progress toward it (including perks granted for free by the
# random-perk power-up), so a re-purchase after going down starts from zero.
$scoreboard players set @s {ns}.zb.perkpaid.$(perk_id) 0

# Call perk-specific effect function
$function {ns}:v{version}/zombies/perks/apply/$(perk_id)
""")

	## Per-perk effect functions (generated from top-level metadata)
	for perk_id, perk_data in PERK_DEFINITIONS.items():
		extra_commands: str = "\n".join(
			command.replace("{ns}", ns)
			for command in perk_data.get("commands", [])
		)
		# Split the emoji prefix out of the colored component (emojis stay uncolored in chat)
		msg_emoji, msg_text = perk_data["message"].split(" ", 1)
		write_versioned_function(f"zombies/perks/apply/{perk_id}", f"""
{extra_commands}
tellraw @s [{MGS_TAG},"{msg_emoji} ",{{"text":"{msg_text}","color":"{perk_data["message_color"]}"}}]
""")

	## Lose all perks: called when a player goes down
	lose_all_lines: list[str] = []
	for perk_id, perk_data in PERK_DEFINITIONS.items():
		removal = perk_data.get("removal_commands", [])
		if removal:
			for cmd in removal:
				lose_all_lines.append(
					f"execute if score @s {ns}.zb.perk.{perk_id} matches 1 run {cmd.replace('{ns}', ns)}"
				)
		# Skip score reset for perks with persistent_score=True (e.g. quick_revive manages its own score)
		if not perk_data.get("persistent_score", False):
			lose_all_lines.append(f"scoreboard players set @s {ns}.zb.perk.{perk_id} 0")
	lose_all_body = "\n".join(lose_all_lines)
	write_versioned_function("zombies/perks/lose_all", f"""
# Remove all perk effects and reset scoreboard tracking
{lose_all_body}
tellraw @s [{MGS_TAG},{{"text":"All perks lost!","color":"red"}}]

# Remove the perk display items from the inventory right away
function {ns}:v{version}/zombies/inventory/refresh_perk_items
""")

	## Hover events (executor: "source" = player)
	perk_hover_message: str = (
		f'[{{"text":"🥤 ","color":"dark_purple"}},'
		f'{{"storage":"{ns}:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true}},'
		f'{{"text":" - Cost: ","color":"gray"}},'
		f'{{"score":{{"name":"#pk_price","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":" points","color":"gray"}}]'
	)
	# Chip-in machines show the next chunk plus the hovering player's own progress
	perk_hover_partial_message: str = (
		f'[{{"text":"🥤 ","color":"dark_purple"}},'
		f'{{"storage":"{ns}:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true}},'
		f'{{"text":" - Chip in: ","color":"gray"}},'
		f'{{"score":{{"name":"#pk_price","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":" points  (","color":"gray"}},'
		f'{{"score":{{"name":"#pk_paid","objective":"{ns}.data"}},"color":"green"}},'
		f'{{"text":"/","color":"gray"}},'
		f'{{"score":{{"name":"#pk_total","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":")","color":"gray"}}]'
	)
	write_versioned_function("zombies/perks/on_hover", f"""
execute store result storage {ns}:temp _pk_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.id
function {ns}:v{version}/zombies/perks/lookup_perk with storage {ns}:temp _pk_hover
function {ns}:v{version}/zombies/perks/get_hover_name
function {ns}:v{version}/zombies/perks/read_price with storage {ns}:temp _pk_data
execute unless score #pk_partial {ns}.data matches 1.. run data modify storage smithed.actionbar:input message set value {{json:{perk_hover_message},priority:"conditional",freeze:5}}
execute if score #pk_partial {ns}.data matches 1.. run data modify storage smithed.actionbar:input message set value {{json:{perk_hover_partial_message},priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")  # noqa: E501

	## Hook into game start: reset perk scoreboards
	map_pool_reset: str = "\n".join(
		f"scoreboard players set #map_perk_{perk_id} {ns}.data 0"
		for perk_id in PERK_DEFINITIONS
	)
	write_versioned_function("zombies/start", f"""
# Reset perk scoreboards for all known score holders (including offline players).
{perk_reset_all_players}

# Chip-in progress never carries between games
{perkpaid_reset_all_players}

# Shared random-perk pool: clear the "perk present on map" flags (repopulated by perks/setup)
{map_pool_reset}

# Clean slate for the joining players: perk effects survive a game that ended without a proper stop,
# and the special.* scores can just as well have come from a multiplayer class or the debug menu.
{perk_effects_teardown(ns, f"@a[scores={{{ns}.zb.in_game=1}}]")}
""")

	## Quick Revive solo pricing: 500 when alone, map price otherwise. Re-checked on join/leave.
	write_versioned_function("zombies/perks/update_quick_revive_price", f"""
# Count alive in-game players
execute store result score #qr_players {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]

# Solo (or none): discounted to 500
execute if score #qr_players {ns}.data matches ..1 run scoreboard players set @e[tag={ns}.pk_quick_revive] {ns}.zb.perk.price 500

# Two or more: restore each machine's map-defined price
execute if score #qr_players {ns}.data matches 2.. as @e[tag={ns}.pk_quick_revive] run scoreboard players operation @s {ns}.zb.perk.price = @s {ns}.zb.perk.base_price
""")

	## Hook into preload_complete: setup perk machines
	write_versioned_function("zombies/preload_complete", f"""
# Setup perk machines
execute if data storage {ns}:zombies game.map.perks[0] run function {ns}:v{version}/zombies/perks/setup

# Apply initial Quick Revive solo pricing
execute if data storage {ns}:zombies game.map.perks[0] run function {ns}:v{version}/zombies/perks/update_quick_revive_price
""")

	## Hook into game tick: keep Quick Revive solo price in sync as players join/leave (every ~1s)
	write_versioned_function("zombies/game_tick", f"""
scoreboard players add #qr_price_tick {ns}.data 1
execute if score #qr_price_tick {ns}.data matches 20.. run scoreboard players set #qr_price_tick {ns}.data 0
execute if score #qr_price_tick {ns}.data matches 0 run function {ns}:v{version}/zombies/perks/update_quick_revive_price
""")

	## Hook into stop: remove perk effects.
	## Selector note: game.py's stop hook has already zeroed zb.in_game by the time these lines run,
	## so a `scores={zb.in_game=1}` selector here matches nobody. The zombies team is never left, so
	## it is what still identifies the players of the game being torn down.
	write_versioned_function("zombies/stop", f"""
# Reset perk effects
{perk_effects_teardown(ns, f"@a[team={ns}.zombies]")}

# Reset perk scoreboards for all known score holders (including offline players).
{perk_reset_all_players}
{perkpaid_reset_all_players}
""")
