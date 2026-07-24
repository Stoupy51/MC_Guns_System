
# Perk Machine System
# Stationary machines where players buy gameplay-enhancing perks.
# Available perks and their behavior are defined in PERK_DEFINITIONS.
from stewbeet import JsonDict, Mem, write_load_file, write_tag, write_versioned_function

from ...config.stats import CAPACITY, REMAINING_BULLETS
from ..helpers import MGS_TAG, reset_special_scores_lines
from ..stamina import STAM_MAX
from .common import deny_not_enough_points_body, deny_requires_power_body, game_active_guard_cmd
from .revive import SOLO_QR_MAX

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
		# Going down strips the active tag (or a doppelganger would still auto-revive off a Quick
		# Revive they no longer own). The score drops to 0 (rebuy allowed) UNLESS the solo uses are
		# exhausted, where score 1 keeps the machine blocked (solo_qr_complete manages that state) —
		# which is also why persistent_score=True: lose_all must not blanket-reset the score.
		"removal_commands": [
			"tag @s remove {ns}.perk.quick_revive",
			f"execute unless score @s {{ns}}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {{ns}}.zb.perk.quick_revive 0",
		],
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
		# Owner-only speed-ups keyed off the special score. Base factor is x2 (no official BO4 number;
		# "about half the time" ≈ 2x, matching the music_box_short jingle ratio) — EXCEPT Pack-a-Punch,
		# which is x3 because its 300-tick animation is already long. All wired:
		#  - Trap cooldown x0.75            (traps.py apply_timeslip_cd)
		#  - Mystery Box spin x2            (mystery_box.py, mb.timeslip flag)
		#  - Pack-a-Punch anim x3           (pap.py: anim/step_timeslip runs 3 steps/tick, preserving
		#                                    every exact-tick phase trigger; jingle_sting_short asset)
		#  - Grenade/equipment throw x0.5   (raycast.py: halves the fire cooldown for grenade weapons)
		"commands": [
			"scoreboard players set @s {ns}.special.timeslip 1",
		],
		"removal_commands": [
			"scoreboard players set @s {ns}.special.timeslip 0",
		],
	},
	"electric_cherry": {
		"display_name": "Electric Cherry",
		"message": "🍒 Electric Cherry! Reloads discharge a shock",
		"message_color": "blue",
		"text_color": "blue",
		# Reload discharge is wired through the on_reload signal (electric_cherry_on_reload); the perk
		# only needs to raise the special flag. Shock size scales with how empty the mag was.
		"commands": [
			"scoreboard players set @s {ns}.special.electric_cherry 1",
		],
		"removal_commands": [
			"scoreboard players set @s {ns}.special.electric_cherry 0",
		],
	},
	"tombstone": {
		"display_name": "Tombstone",
		"message": "🪦 Tombstone! Recover your gear if you bleed out",
		"message_color": "yellow",
		"text_color": "gold",
		# No purchase-time effect. On going down a tombstone marker is spawned (revive/on_down); if the
		# owner bleeds out, they get 60s after the round respawn to walk back and recover their perks +
		# weapons (Tombstone itself excluded). Disabled solo. See the tombstone_* functions.
	},
	"whos_who": {
		"display_name": "Who's Who",
		"message": "👥 Who's Who! Play on as a doppelganger when downed",
		"message_color": "aqua",
		"text_color": "dark_aqua",
		# No purchase-time effect. On going down the owner keeps playing as a doppelganger (revive/on_down
		# branch) with just a pistol; the body drops as a NORMAL revivable downed mannequin that any
		# alive player — including the owner — can revive. Works solo (and takes priority over solo
		# Quick Revive). See whos_who.py.
	},
	"dying_wish": {
		"display_name": "Dying Wish",
		"message": "⚔ Dying Wish! Cheat death with a berserk",
		"message_color": "blue",
		"text_color": "blue",
		# No purchase-time effect: the behaviour triggers when the owner would go down (revive/on_down
		# intercepts to dying_wish_trigger, off cooldown). Ownership is read straight off zb.perk.dying_wish.
	},
	"widows_wine": {
		"display_name": "Widow's Wine",
		"message": "🕸 Widow's Wine! Web grenades & webbing melee",
		"message_color": "dark_red",
		"text_color": "dark_red",
		# Passive web-on-hurt + stronger knife read the special flag directly (hurt_player.py, melee
		# attribute below). The grenade slot is swapped to web grenades by inventory/replenish paths.
		"commands": [
			"scoreboard players set @s {ns}.special.widows_wine 1",
			# Stronger knife while owned (small flat melee bonus, BO3 Widow's Wine melee buff)
			"attribute @s minecraft:attack_damage modifier add {ns}:widows_wine 6 add_value",
			# Immediately convert the current lethal slot to web grenades (widows_wine flag is set
			# above, so loot_replace_lethal routes hotbar.7 to i/web_grenade).
			"function {ns}:v{version}/zombies/inventory/loot_replace_lethal",
			"item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_2",
			'function {ns}:v{version}/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}',
		],
		"removal_commands": [
			"scoreboard players set @s {ns}.special.widows_wine 0",
			"attribute @s minecraft:attack_damage modifier remove {ns}:widows_wine",
		],
	},
}


# Recommended buy price per perk, used when a machine's editor `price` field is left at -1
# (the auto-resolve default). Keyed by perk_id; any perk not listed falls back to 2000.
RECOMMENDED_PRICES: dict[str, int] = {
	"juggernog": 2500, "speed_cola": 3000, "double_tap": 2000, "quick_revive": 1500,
	"mule_kick": 4000, "stamin_up": 2000, "phd_flopper": 2000, "deadshot": 1500,
	"timeslip": 1500, "electric_cherry": 2000, "tombstone": 2000, "whos_who": 2000,
	"dying_wish": 2000, "widows_wine": 4000,
}

# Detailed perk descriptions, shown as lore on the mini perk items in the inventory. One list entry
# per lore line (kept short so they read cleanly in the tooltip). Keyed by perk_id.
PERK_DESCRIPTIONS: dict[str, list[str]] = {
	"juggernog": ["Raises your max health to 40 (x4).", "Survive far more hits before going down."],
	"speed_cola": ["Reload all your weapons much faster.", "About twice the reload speed."],
	"double_tap": ["Fires an extra bullet with every shot.", "Roughly doubles your damage output."],
	"quick_revive": ["Revive downed teammates faster.", "Solo: revives you after you go down."],
	"mule_kick": ["Carry a third weapon.", "Unlocks an extra weapon slot."],
	"stamin_up": ["Move faster and sprint for longer.", "+7% move speed, double sprint endurance."],
	"phd_flopper": ["Immune to fall and self-explosive damage.", "Dive to prone to set off a blast."],
	"deadshot": ["Aim snaps toward zombie heads.", "Tighter hipfire spread and less recoil."],
	"timeslip": ["Machines and power-ups spin faster.", "Pack-a-Punch, box & Wunderfizz speed up.", "Grenades throw on a shorter cooldown."],
	"electric_cherry": ["Reloading discharges a shockwave.", "Damages and stuns nearby zombies.", "Stronger the emptier your magazine."],
	"tombstone": ["If you bleed out, leave a Tombstone.", "Return to it the next round to recover", "your perks and full inventory."],
	"whos_who": ["When downed, fight on as a clone.", "Revive your own body to fully recover.", "Works solo or co-op."],
	"dying_wish": ["Cheat death when you would go down.", "Brief berserk (resistance & strength),", "then drop to 1 HP. Long cooldown."],
	"widows_wine": ["Grenades become sticky web grenades.", "Being hit bursts webbing around you.", "Stronger melee knife."],
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
execute as {selector} run attribute @s minecraft:attack_damage modifier remove {ns}:widows_wine
execute as {selector} run attribute @s minecraft:attack_damage modifier remove {ns}:dying_wish
tag {selector} remove {ns}.dying_wish_active
scoreboard players set {selector} {ns}.zb.dw_uses 0
scoreboard players set {selector} {ns}.zb.dw_cd 0
scoreboard players set {selector} {ns}.zb.dw_timer 0
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
			command.replace("{ns}", ns).replace("{version}", version)
			for command in perk_data.get("commands", [])
		)
		# Split the emoji prefix out of the colored component (emojis stay uncolored in chat)
		msg_emoji, msg_text = perk_data["message"].split(" ", 1)
		write_versioned_function(f"zombies/perks/apply/{perk_id}", f"""
{extra_commands}
tellraw @s [{MGS_TAG},"{msg_emoji} ",{{"text":"{msg_text}","color":"{perk_data["message_color"]}"}}]
""")

	## ── Electric Cherry ─────────────────────────────────────────────────────────
	# A reload discharges an electric shock around the owner. Size (radius + damage) scales with how
	# empty the magazine was at reload start (capacity - remaining_bullets), so dry reloads hit hard.
	# Anti-spam: after a discharge the next one needs either a full 10s cooldown, OR 5s + a dry reload
	# (remaining == 0). The last-shock time is a gametime stamp (monotonic, survives /reload).
	write_load_file(f"""
# Electric Cherry: last-discharge gametime stamp (anti-spam cooldown)
scoreboard objectives add {ns}.zb.ec_last dummy
# Widow's Wine: last web-on-hurt burst gametime stamp (passive cooldown)
scoreboard objectives add {ns}.zb.ww_last dummy
# Dying Wish: use count (escalates cooldown), cooldown countdown, and active berserk timer
scoreboard objectives add {ns}.zb.dw_uses dummy
scoreboard objectives add {ns}.zb.dw_cd dummy
scoreboard objectives add {ns}.zb.dw_timer dummy
# Tombstone: marker state (0 pending / 1 active) + recovery countdown; the marker also carries the
# owner's zb.downed_id so the existing downed_id_match predicate can select it.
scoreboard objectives add {ns}.zb.ts.state dummy
scoreboard objectives add {ns}.zb.ts.timer dummy
# Tombstone: per-perk snapshot of what the owner had when they went down (restored on recovery)
{chr(10).join(f"scoreboard objectives add {ns}.zb.tsp.{pid} dummy" for pid in PERK_DEFINITIONS)}
""")

	## Signal handler on on_reload (@s = the reloading player). Registered into the global reload
	## signal but no-ops outside a zombies game / for non-owners.
	write_versioned_function("zombies/perks/electric_cherry_on_reload", f"""
execute unless score @s {ns}.zb.in_game matches 1.. run return fail
execute unless score @s {ns}.special.electric_cherry matches 1 run return fail

# Bullets discharged = capacity - remaining (read capacity from the reload signal payload)
execute store result score #ec_cap {ns}.data run data get storage {ns}:signals on_reload.weapon.stats.{CAPACITY}
execute store result score #ec_rem {ns}.data run scoreboard players get @s {ns}.{REMAINING_BULLETS}
execute if score #ec_rem {ns}.data matches ..-1 run scoreboard players set #ec_rem {ns}.data 0
scoreboard players operation #ec_used {ns}.data = #ec_cap {ns}.data
scoreboard players operation #ec_used {ns}.data -= #ec_rem {ns}.data
execute if score #ec_used {ns}.data matches ..0 run return fail

# Cooldown gate: since = now - last discharge. Allowed if since>=200 (10s), or since>=100 (5s) on a dry reload.
execute store result score #ec_now {ns}.data run time query gametime
scoreboard players operation #ec_since {ns}.data = #ec_now {ns}.data
scoreboard players operation #ec_since {ns}.data -= @s {ns}.zb.ec_last
scoreboard players set #ec_ok {ns}.data 0
execute if score #ec_since {ns}.data matches 200.. run scoreboard players set #ec_ok {ns}.data 1
execute if score #ec_since {ns}.data matches 100.. if score #ec_rem {ns}.data matches 0 run scoreboard players set #ec_ok {ns}.data 1
execute if score #ec_ok {ns}.data matches 0 run return fail

# Fire the discharge and stamp the time
scoreboard players operation @s {ns}.zb.ec_last = #ec_now {ns}.data
execute at @s run function {ns}:v{version}/zombies/perks/electric_cherry_shock
""", tags=[f"{ns}:signals/on_reload"])

	## The discharge itself. @s = owner, executed at the owner. #ec_used/#ec_cap set by the caller.
	## Also fired when an owner goes down (revive on_down prepares those scores from a full mag).
	write_versioned_function("zombies/perks/electric_cherry_shock", f"""
# Feedback
particle minecraft:electric_spark ~ ~1 ~ 2 1 2 0.25 80 force @a[distance=..48]
particle minecraft:flash{{color:[1.0,1.0,1.0,1.0]}} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..48]
playsound minecraft:entity.lightning_bolt.thunder player @a[distance=..32] ~ ~ ~ 0.6 1.6
playsound minecraft:block.beacon.deactivate player @a[distance=..24] ~ ~ ~ 0.6 2

# Radius (blocks x1000): 2500 + 3500 * used/cap  ->  2.5 .. 6.0 blocks
scoreboard players operation #ec_r {ns}.data = #ec_used {ns}.data
scoreboard players operation #ec_r {ns}.data *= #3500 {ns}.data
scoreboard players operation #ec_r {ns}.data /= #ec_cap {ns}.data
scoreboard players add #ec_r {ns}.data 2500
execute store result storage {ns}:temp _ec.radius float 0.001 run scoreboard players get #ec_r {ns}.data

# Damage as a fraction of each zombie's max health (percent x0.01): 40 + 60 * used/cap  ->  0.40 .. 1.00
scoreboard players operation #ec_frac {ns}.data = #ec_used {ns}.data
scoreboard players operation #ec_frac {ns}.data *= #60 {ns}.data
scoreboard players operation #ec_frac {ns}.data /= #ec_cap {ns}.data
scoreboard players add #ec_frac {ns}.data 40
execute store result storage {ns}:temp _ec.scale double 0.01 run scoreboard players get #ec_frac {ns}.data

function {ns}:v{version}/zombies/perks/electric_cherry_damage with storage {ns}:temp _ec
""")

	## Select zombies inside the (macro) radius and shock each. @s/pos = owner.
	write_versioned_function("zombies/perks/electric_cherry_damage", f"""
$execute as @e[tag={ns}.zombie_round,distance=..$(radius)] run function {ns}:v{version}/zombies/perks/electric_cherry_hit {{scale:"$(scale)"}}
""")

	## Per-zombie shock: damage (fraction of max health, macro scale) + brief stun. @s = zombie.
	write_versioned_function("zombies/perks/electric_cherry_hit", f"""
$execute store result storage {ns}:temp _ec_dmg.amount int 1 run attribute @s minecraft:max_health get $(scale)
data modify storage {ns}:temp _ec_dmg.type set value "minecraft:lightning_bolt"
particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.1 12
effect give @s minecraft:slowness 60 3 true
function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _ec_dmg
""")

	## ── Widow's Wine ────────────────────────────────────────────────────────────
	# Web grenades (grenade framework, GRENADE_TYPE "web") + a passive web burst when the owner is hurt
	# + a knife melee bump (attribute, in the perk def). The web itself: heavy slowness/weakness + a
	# little damage to every zombie in range. Shared by the thrown grenade (grenade/detonate_web) and
	# the on-hurt passive so the effect is defined once.

	## Web burst: @s/pos = the burst center. Macro radius (blocks). Roots + lightly damages zombies.
	write_versioned_function("zombies/perks/widows_web_burst", f"""
$execute as @e[tag={ns}.zombie_round,distance=..$(radius)] run function {ns}:v{version}/zombies/perks/widows_web_hit
""")

	## Per-zombie webbing: 5s stun (heavy slowness) + weakness, cobweb particle, light damage. @s = zombie.
	## NOTE /effect give durations are in SECONDS, not ticks — 5 = 5s (was 400 = ~6.7min "frozen forever").
	write_versioned_function("zombies/perks/widows_web_hit", f"""
effect give @s minecraft:slowness 5 5 true
effect give @s minecraft:weakness 5 2 true
particle minecraft:item{{item:"minecraft:cobweb"}} ~ ~0.5 ~ 0.3 0.5 0.3 0.05 8
execute store result storage {ns}:temp _ww_dmg.amount int 1 run attribute @s minecraft:max_health get 0.15
data modify storage {ns}:temp _ww_dmg.type set value "minecraft:generic"
function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _ww_dmg
""")

	## Passive: when a Widow's Wine owner is hurt, consume one web grenade and burst webbing around
	## themselves (no self-damage — the burst only targets zombies). Called from hurt_player on_hurt.
	## Internal 2s cooldown (gametime stamp) so a single flurry of hits doesn't drain the whole stock.
	write_versioned_function("zombies/perks/widows_on_hurt", f"""
# Need at least one web grenade in the lethal slot (grenade_type lives under the item's stats compound)
execute unless items entity @s hotbar.7 *[custom_data~{{{ns}:{{stats:{{grenade_type:"web"}}}}}}] run return fail

# 2s (40t) internal cooldown
execute store result score #ww_now {ns}.data run time query gametime
scoreboard players operation #ww_since {ns}.data = #ww_now {ns}.data
scoreboard players operation #ww_since {ns}.data -= @s {ns}.zb.ww_last
execute if score #ww_since {ns}.data matches ..39 run return fail
scoreboard players operation @s {ns}.zb.ww_last = #ww_now {ns}.data

# Consume one web grenade + burst webbing around the player
item modify entity @s hotbar.7 {ns}:v{version}/grenade/consume_one
particle minecraft:item{{item:"minecraft:cobweb"}} ~ ~1 ~ 0.8 0.8 0.8 0.1 40 force @a[distance=..48]
playsound minecraft:block.wool.place player @a[distance=..32] ~ ~ ~ 1 0.7
execute store result storage {ns}:temp _web.radius float 1 run scoreboard players get #4 {ns}.data
execute at @s run function {ns}:v{version}/zombies/perks/widows_web_burst with storage {ns}:temp _web
""")

	## ── Dying Wish ──────────────────────────────────────────────────────────────
	# Instead of entering the downed state, the owner cheats death: teleport back to the death spot,
	# restore, and go BERSERK (invulnerable + greatly increased melee) for 9s, then be left at 1 HP.
	# Per-use escalating cooldown (60s first use, +60s each subsequent). Highest priority at on_down.
	# Triggered from revive/on_down (top), which is why there is no purchase-time effect.

	## Trigger: @s = the player who would have gone down (already vanilla-respawned; LastDeathLocation set).
	write_versioned_function("zombies/perks/dying_wish_trigger", f"""
# Not a real down — undo the downs++ that on_respawn added before calling on_down
scoreboard players remove @s {ns}.zb.downs 1

# Count the use and set the escalating cooldown (60s * uses = 1200t * uses)
scoreboard players add @s {ns}.zb.dw_uses 1
scoreboard players operation @s {ns}.zb.dw_cd = @s {ns}.zb.dw_uses
scoreboard players operation @s {ns}.zb.dw_cd *= #1200 {ns}.data

# Teleport back to the death location (reuse the revive tp macro)
execute store result storage {ns}:temp rv_x double 0.001 run data get entity @s LastDeathLocation.pos[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get entity @s LastDeathLocation.pos[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get entity @s LastDeathLocation.pos[2] 1000
function {ns}:v{version}/zombies/revive/tp_revive_pos with storage {ns}:temp

# Restore: adventure mode, full health (respect Juggernog), stamina
gamemode adventure @s
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s {ns}.stam_seen 0

# Berserk for 9s (180t): invulnerable (resistance V) + one-shot melee + mobility, and a big melee attribute
scoreboard players set @s {ns}.zb.dw_timer 180
tag @s add {ns}.dying_wish_active
effect give @s minecraft:resistance 180 4 true
effect give @s minecraft:fire_resistance 180 0 true
effect give @s minecraft:strength 180 4 true
effect give @s minecraft:speed 180 1 true
attribute @s minecraft:attack_damage modifier add {ns}:dying_wish 200 add_value

# Feedback
title @s times 5 40 15
title @s title ["⚔"]
title @s subtitle [{{"text":"DYING WISH — Berserk!","color":"dark_red"}}]
particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.3 80 force @a[distance=..32]
playsound minecraft:item.totem.use player @a[distance=..32] ~ ~ ~ 1 0.8
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"blue"}},{{"text":" refuses to die!","color":"gray"}}]
""")

	## Per-tick berserk countdown (called from player/tick while dw_timer >= 1). @s = player.
	write_versioned_function("zombies/perks/dying_wish_tick", f"""
particle minecraft:crit ~ ~1 ~ 0.4 0.6 0.4 0.05 4 force @a[distance=..24]
scoreboard players remove @s {ns}.zb.dw_timer 1
execute if score @s {ns}.zb.dw_timer matches ..0 run function {ns}:v{version}/zombies/perks/dying_wish_end
""")

	## Berserk ends: strip the buffs and leave the player at 1 HP. @s = player.
	write_versioned_function("zombies/perks/dying_wish_end", f"""
attribute @s minecraft:attack_damage modifier remove {ns}:dying_wish
effect clear @s minecraft:resistance
effect clear @s minecraft:fire_resistance
effect clear @s minecraft:strength
effect clear @s minecraft:speed
tag @s remove {ns}.dying_wish_active
scoreboard players set @s {ns}.zb.dw_timer 0

# Left at 1 HP (BO behaviour). /data can't write a player's Health and the max-health clamp trick
# doesn't reliably pull current HP down (both attribute sets collapse in one tick), so deal an exact
# (Health - 1) hit with generic_kill — it bypasses armor, resistance and effects, landing the player
# on precisely 1 HP. Health*1000 for sub-HP precision; skip if already at/below 1.
execute store result score #dw_hp {ns}.data run data get entity @s Health 1000
scoreboard players remove #dw_hp {ns}.data 1000
execute if score #dw_hp {ns}.data matches 1.. run function {ns}:v{version}/zombies/perks/dying_wish_to_1
title @s times 3 25 10
title @s subtitle [{{"text":"...barely alive.","color":"gray"}}]
""")

	## Deal exactly (Health - 1) damage to land the player on 1 HP. #dw_hp = (Health-1)*1000. @s = player.
	## generic_kill has no source entity, so this never trips the entity_hurt_player on_hurt handler.
	write_versioned_function("zombies/perks/dying_wish_to_1", f"""
execute store result storage {ns}:temp _dw_dmg.amount double 0.001 run scoreboard players get #dw_hp {ns}.data
data modify storage {ns}:temp _dw_dmg.type set value "minecraft:generic_kill"
function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _dw_dmg
""")

	## ── Tombstone ───────────────────────────────────────────────────────────────
	# On going down, a tombstone marker spawns at the death spot (holding a snapshot of the owner's
	# perks). Revived → the marker is discarded. Bled out → the inventory is snapshotted, and after the
	# round respawn the owner has 60s to walk back to the marker and recover their perks + weapons
	# (Tombstone itself excluded). Disabled solo. Called from revive/on_down, revive_complete,
	# bleed_out, and do_round_respawn.
	# quick_revive: score 1 can also mean "solo uses exhausted" (rebuy-block) with no active tag —
	# only snapshot a QR that is actually active, or the recovery would grant one back for free.
	ts_snapshot: str = "\n".join(
		f"execute store success score @s {ns}.zb.tsp.{pid} if entity @s[tag={ns}.perk.quick_revive]"
		if pid == "quick_revive"
		else f"scoreboard players operation @s {ns}.zb.tsp.{pid} = @s {ns}.zb.perk.{pid}"
		for pid in PERK_DEFINITIONS
	)
	ts_clear: str = "\n".join(f"scoreboard players set @s {ns}.zb.tsp.{pid} 0" for pid in PERK_DEFINITIONS)

	# Reapply-effect (no chat message) for perks with commands — used when recovering from a tombstone.
	for pid, pdata in PERK_DEFINITIONS.items():
		cmds: str = "\n".join(c.replace("{ns}", ns).replace("{version}", version) for c in pdata.get("commands", []))
		if cmds:
			write_versioned_function(f"zombies/perks/reapply/{pid}", cmds)

	ts_restore_perks_lines: list[str] = []
	for pid, pdata in PERK_DEFINITIONS.items():
		if pid == "tombstone":
			continue  # Tombstone excludes itself from recovery (BO behaviour) — must be rebought
		ts_restore_perks_lines.append(f"execute if score @s {ns}.zb.tsp.{pid} matches 1 run scoreboard players set @s {ns}.zb.perk.{pid} 1")
		if pdata.get("commands"):
			ts_restore_perks_lines.append(f"execute if score @s {ns}.zb.tsp.{pid} matches 1 run function {ns}:v{version}/zombies/perks/reapply/{pid}")
	ts_restore_perks: str = "\n".join(ts_restore_perks_lines)

	## Called from revive/on_down BEFORE lose_all (@s = player, death pos in temp rv_x/rv_y/rv_z).
	## Skips solo games. Snapshots perks and spawns the (pending) tombstone marker.
	write_versioned_function("zombies/perks/tombstone_on_down", f"""
# Tombstone is disabled solo (a solo bleed-out is game over — nothing to recover to)
execute store result score #ts_ingame {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}}]
execute if score #ts_ingame {ns}.data matches ..1 run return 0

# Snapshot which perks the owner had (restored on recovery)
{ts_snapshot}

# Spawn the tombstone marker at the player, tag it with the owner's downed_id, then move to death spot
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.tombstone","{ns}.tombstone_new","{ns}.gm_entity"],Glowing:true,billboard:"vertical",teleport_duration:1,item:{{id:"minecraft:skeleton_skull",count:1}},item_display:"ground",transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.3f,0f],scale:[1.2f,1.2f,1.2f]}}}}
scoreboard players operation @n[tag={ns}.tombstone_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id
scoreboard players set @n[tag={ns}.tombstone_new] {ns}.zb.ts.state 0
scoreboard players set @n[tag={ns}.tombstone_new] {ns}.zb.ts.timer 0
function {ns}:v{version}/zombies/perks/tombstone_tp with storage {ns}:temp
tag @e[tag={ns}.tombstone_new] remove {ns}.tombstone_new
""")

	## Macro: move the freshly-spawned marker to the death location (rv_x/rv_y/rv_z from on_down).
	write_versioned_function("zombies/perks/tombstone_tp", f"""
$tp @n[tag={ns}.tombstone_new] $(rv_x) $(rv_y) $(rv_z)
""")

	## Called from revive_complete (@s = revived player; #my_downed_id already set). The owner was
	## revived, so discard the pending marker and the perk snapshot — nothing to recover.
	write_versioned_function("zombies/perks/tombstone_on_revived", f"""
kill @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match]
{ts_clear}
""")

	## Called from bleed_out (@s = player; #my_downed_id already set). If a marker exists for this
	## player, snapshot their current inventory (still intact during the downed phase) for recovery.
	write_versioned_function("zombies/perks/tombstone_on_bleed_out", f"""
execute unless entity @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match] run return 0
execute store result storage {ns}:temp _ts_id.id int 1 run scoreboard players get @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/perks/tombstone_snapshot_inv with storage {ns}:temp _ts_id
""")

	## Macro: store @s Inventory keyed by downed_id.
	write_versioned_function("zombies/perks/tombstone_snapshot_inv", f"""
$data modify storage {ns}:zombies tombstone_inv."$(id)" set from entity @s Inventory
""")

	## Called from do_round_respawn (@s = respawning player). If this player has a pending tombstone
	## marker (they bled out with Tombstone), activate it and start the 60s recovery timer.
	write_versioned_function("zombies/perks/tombstone_on_respawn", f"""
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute unless entity @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match] run return 0
scoreboard players set @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match] {ns}.zb.ts.state 1
scoreboard players set @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match] {ns}.zb.ts.timer 1200
title @s times 5 40 15
title @s subtitle [{{"text":"Return to your 🪦 within 60s to recover your gear!","color":"gold"}}]
""")

	## Per-tick for an ACTIVE tombstone marker (@s = marker, at it). Counts down, then checks whether
	## the owning player is standing on it to recover. Hooked into game_tick.
	write_versioned_function("zombies/perks/tombstone_marker_tick", f"""
particle minecraft:soul ~ ~0.5 ~ 0.25 0.4 0.25 0.01 3 force @a[distance=..48]
particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.15 0.2 0.15 0.005 1 force @a[distance=..48]

# Count down; expire (despawn + drop the inventory snapshot) when the timer runs out
scoreboard players operation @s {ns}.zb.ts.timer -= #tick_delta {ns}.data
execute if score @s {ns}.zb.ts.timer matches ..0 run return run function {ns}:v{version}/zombies/perks/tombstone_expire

# Owner standing within 2 blocks (alive, in-game, not downed) → recover
scoreboard players operation #ts_mid {ns}.data = @s {ns}.zb.downed_id
execute as @a[distance=..2,gamemode=!spectator,scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}}] if score @s {ns}.zb.downed_id = #ts_mid {ns}.data run function {ns}:v{version}/zombies/perks/tombstone_collect
""")

	## Marker expired (@s = marker): drop the stored inventory and despawn.
	write_versioned_function("zombies/perks/tombstone_expire", f"""
execute store result storage {ns}:temp _ts_id.id int 1 run scoreboard players get @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/perks/tombstone_clear_inv with storage {ns}:temp _ts_id
kill @s
""")

	## Macro: drop a stored inventory snapshot by id.
	write_versioned_function("zombies/perks/tombstone_clear_inv", f"""
$data remove storage {ns}:zombies tombstone_inv."$(id)"
""")

	## Recover (@s = the owner standing on their tombstone): restore perks + inventory, despawn marker.
	write_versioned_function("zombies/perks/tombstone_collect", f"""
# Restore perks (Tombstone excluded) and re-apply their effects silently
{ts_restore_perks}

# Restore max health for the restored Juggernog state
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40

# Restore the snapshotted inventory (weapons/mags/grenades) into the exact original slots via the
# shared restore system (players can't be data-modified), then drop the snapshot
execute store result storage {ns}:temp _ts_id.id int 1 run scoreboard players get @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/perks/tombstone_load_snapshot with storage {ns}:temp _ts_id
function {ns}:v{version}/zombies/inventory/restore_inventory

# Rebuild the perk display items now that ownership is restored
function {ns}:v{version}/zombies/inventory/refresh_perk_items

# Clear the snapshot scores and despawn the marker (id-matched)
{ts_clear}
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
kill @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match]

# Feedback
title @s times 5 40 15
title @s title ["🪦"]
title @s subtitle [{{"text":"Gear recovered!","color":"green"}}]
playsound minecraft:block.respawn_anchor.charge player @a[distance=..24] ~ ~ ~ 1 1.2
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"green"}},{{"text":" recovered their gear from a tombstone!","color":"gray"}}]
""")

	## Macro: load a snapshot by id into the shared restore buffer, then drop the snapshot.
	write_versioned_function("zombies/perks/tombstone_load_snapshot", f"""
$data modify storage {ns}:temp _restore.items set from storage {ns}:zombies tombstone_inv."$(id)"
$data remove storage {ns}:zombies tombstone_inv."$(id)"
""")

	## Hook: tick active tombstone markers.
	write_versioned_function("zombies/game_tick", f"""
execute as @e[tag={ns}.tombstone,scores={{{ns}.zb.ts.state=1}}] at @s run function {ns}:v{version}/zombies/perks/tombstone_marker_tick
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
		f'{{"text":" points (","color":"gray"}},'
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
""")

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
