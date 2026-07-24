
# ruff: noqa: E501
# Map-editor element and mode definitions (data only; the generator lives in map_editor.py).
from dataclasses import dataclass
from dataclasses import field as dc_field
from typing import Any

from stewbeet import JsonDict

from .zombies.perks import PERK_DEFINITIONS, RECOMMENDED_PRICES

MAX_MAPS = 50

# Perk reference lines for the perk_machine tooltips, generated from the perk registry so they can
# never drift out of sync with the actual perks (ids grouped 5/line, prices as "Name N" grouped 3/line).
_PERK_IDS: list[str] = list(PERK_DEFINITIONS.keys())
_PERK_ID_DOC: str = (
	"Perk granted by this machine:\n"
	+ "\n".join(" · ".join(_PERK_IDS[i:i + 5]) for i in range(0, len(_PERK_IDS), 5))
	+ "\n\nThe Random Perk power-up and Der Wunderfizz only roll perks that have a\n"
	"machine placed on this map (unless a Wunderfizz has all_perks set), so\n"
	"which perks you place here shapes what they can grant."
)
_PERK_PRICE_PAIRS: list[str] = [f'{PERK_DEFINITIONS[pid].display_name} {RECOMMENDED_PRICES.get(pid, 2000)}' for pid in _PERK_IDS]
_PERK_PRICE_DOC: str = (
	"Cost in points to buy this perk.\n"
	"Leave at -1 to auto-resolve the recommended price from perk_id.\n"
	"Recommended prices:\n"
	+ "\n".join(" · ".join(_PERK_PRICE_PAIRS[i:i + 3]) for i in range(0, len(_PERK_PRICE_PAIRS), 3))
)

# Element Definitions ───────────────────────────────────────────
@dataclass(frozen=True)
class ElementDef:
	""" One placeable map element: how its marker looks and how it is saved. """
	name: str
	color: str
	particle: list[float]
	particle_scale: float
	has_rotation: bool
	egg_model: str
	save_type: str
	""" "base" (single, handled specially), "spawn" ([x,y,z,yaw] list), "point" ([x,y,z] list),
	"zb_object" (compound objects with pos/rotation/group_id + extra fields), "enemy", "config",
	"start_command", "respawn_command". """
	emoji: str
	save_path: str = ""
	""" Dotted key under the mode's storage where instances are written (empty for base/config). """
	defaults: JsonDict = dc_field(default_factory=dict[str, Any])
	""" Per-element default config, written on placement (only zb_object elements use it). """
	config_uses_default_function: bool = False
	requires_offhand_block: bool = False


# All element types across all modes.
ALL_ELEMENTS: dict[str, ElementDef] = {
	"base_coordinates": ElementDef(name="Base Coordinates", color="light_purple", particle=[1.0, 0.0, 1.0], particle_scale=1.5, has_rotation=False, egg_model="minecraft:endermite_spawn_egg", save_type="base", emoji="⬟"),
	"red_spawn": ElementDef(name="Red Spawn", color="red", particle=[1.0, 0.2, 0.2], particle_scale=1.0, has_rotation=True, egg_model="minecraft:magma_cube_spawn_egg", save_type="spawn", save_path="spawning_points.red", emoji="●"),
	"blue_spawn": ElementDef(name="Blue Spawn", color="blue", particle=[0.2, 0.2, 1.0], particle_scale=1.0, has_rotation=True, egg_model="minecraft:dolphin_spawn_egg", save_type="spawn", save_path="spawning_points.blue", emoji="●"),
	"general_spawn": ElementDef(name="General Spawn", color="yellow", particle=[1.0, 1.0, 0.2], particle_scale=1.0, has_rotation=True, egg_model="minecraft:blaze_spawn_egg", save_type="spawn", save_path="spawning_points.general", emoji="●"),
	"out_of_bounds": ElementDef(name="Out of Bounds", color="dark_red", particle=[0.6, 0.0, 0.0], particle_scale=1.0, has_rotation=False, egg_model="minecraft:spider_spawn_egg", save_type="point", save_path="out_of_bounds", emoji="☠"),
	"boundary": ElementDef(name="Boundary Corner", color="gray", particle=[0.8, 0.8, 0.8], particle_scale=1.0, has_rotation=False, egg_model="minecraft:skeleton_spawn_egg", save_type="point", save_path="boundaries", emoji="◻"),
	"search_and_destroy": ElementDef(name="S&D Objective", color="gold", particle=[1.0, 0.6, 0.0], particle_scale=1.0, has_rotation=False, egg_model="minecraft:fox_spawn_egg", save_type="point", save_path="search_and_destroy", emoji="💣"),
	"domination": ElementDef(name="Domination Point", color="green", particle=[0.0, 1.0, 0.0], particle_scale=1.0, has_rotation=False, egg_model="minecraft:creeper_spawn_egg", save_type="point", save_path="domination", emoji="🏴"),
	"hardpoint": ElementDef(name="Hardpoint Zone", color="dark_purple", particle=[0.5, 0.0, 0.5], particle_scale=1.0, has_rotation=False, egg_model="minecraft:warden_spawn_egg", save_type="point", save_path="hardpoint", emoji="⚡"),
	"start_command": ElementDef(name="Start Command", color="aqua", particle=[0.0, 0.9, 0.9], particle_scale=1.0, has_rotation=False, egg_model="minecraft:allay_spawn_egg", save_type="start_command", save_path="start_commands", emoji="⚙"),
	"respawn_command": ElementDef(name="Respawn Command", color="dark_aqua", particle=[0.0, 0.7, 0.7], particle_scale=1.0, has_rotation=False, egg_model="minecraft:vex_spawn_egg", save_type="respawn_command", save_path="respawn_commands", emoji="↺"),
	# Mission elements
	"mission_spawn": ElementDef(name="Mission Spawn", color="aqua", particle=[0.0, 1.0, 1.0], particle_scale=1.0, has_rotation=True, egg_model="minecraft:villager_spawn_egg", save_type="spawn", save_path="spawning_points.mission", emoji="●"),
	"enemy": ElementDef(name="Enemy", color="red", particle=[1.0, 0.2, 0.2], particle_scale=1.0, has_rotation=False, egg_model="minecraft:pillager_spawn_egg", save_type="enemy", save_path="enemies", emoji="👤", config_uses_default_function=True),
	# Config (utility, no marker)
	"config": ElementDef(name="⚙ Config", color="white", particle=[1.0, 1.0, 1.0], particle_scale=0.5, has_rotation=False, egg_model="minecraft:allay_spawn_egg", save_type="config", emoji="⚙"),
	# Zombies elements (zb_object: compound data with pos/rotation/group_id + extra fields)
	"zombie_spawn": ElementDef(name="Zombie Spawn", color="dark_green", particle=[0.0, 0.5, 0.0], particle_scale=1.0, has_rotation=True, egg_model="minecraft:zombie_spawn_egg", save_type="zb_object", save_path="spawning_points.zombies", emoji="🧟", defaults={"activation_box": []}),
	"player_spawn_zb": ElementDef(name="Player Spawn", color="aqua", particle=[0.0, 1.0, 1.0], particle_scale=1.0, has_rotation=True, egg_model="minecraft:villager_spawn_egg", save_type="zb_object", save_path="spawning_points.players", emoji="●", defaults={}),
	# Special spawns are the "not a regular zombie" spawn set: dog rounds use them today, mini-bosses
	# and other scripted arrivals can reuse them later. A map without any simply never gets those rounds.
	"special_spawn": ElementDef(name="Special Spawn", color="dark_red", particle=[0.6, 0.0, 0.2], particle_scale=1.0, has_rotation=True, egg_model="minecraft:wolf_spawn_egg", save_type="zb_object", save_path="spawning_points.special", emoji="🐺", defaults={"activation_box": []}),
	"wallbuy": ElementDef(name="Wallbuy", color="yellow", particle=[1.0, 1.0, 0.0], particle_scale=1.0, has_rotation=True, egg_model="minecraft:iron_golem_spawn_egg", save_type="zb_object", save_path="wallbuys", emoji="🔫", defaults={"name": "", "price": 1000, "refill_price": 500, "refill_price_pap": 4500, "weapon_id": "m1911", "magazine_id": "m1911_mag"}),
	"door": ElementDef(name="Door", color="gold", particle=[1.0, 0.6, 0.0], particle_scale=1.0, has_rotation=True, egg_model="minecraft:hoglin_spawn_egg", save_type="zb_object", save_path="doors", emoji="🚪", defaults={"name": "Door", "back_name": "Door", "price": 1000, "partial_price": 0, "link_id": 1, "back_group_id": -1, "block": "", "animation": 0, "sound": ""}, requires_offhand_block=True),
	# Trap types: 0 = fire, 1 = electric, 2 = turret
	"trap": ElementDef(name="Trap", color="red", particle=[1.0, 0.2, 0.2], particle_scale=1.0, has_rotation=True, egg_model="minecraft:cave_spider_spawn_egg", save_type="zb_object", save_path="traps", emoji="🔮", defaults={"price": 1000, "type": 0, "duration": 200, "cooldown": 1200, "effect_radius": [3.0, 2.0, 3.0], "offset_pos": [0, 0, 0], "power": True}),
	"perk_machine": ElementDef(name="Perk Machine", color="dark_purple", particle=[0.5, 0.0, 0.5], particle_scale=1.0, has_rotation=True, egg_model="minecraft:witch_spawn_egg", save_type="zb_object", save_path="perks", emoji="🧪", defaults={"name": "", "price": -1, "partial_price": 0, "perk_id": "juggernog", "power": True, "display_item": "", "item_model": ""}),
	"wunderfizz": ElementDef(name="Der Wunderfizz", color="gold", particle=[1.0, 0.7, 0.0], particle_scale=1.0, has_rotation=True, egg_model="minecraft:bee_spawn_egg", save_type="zb_object", save_path="wunderfizz", emoji="🎰", defaults={"name": "Der Wunderfizz", "price": 1500, "power": True, "all_perks": False, "can_start_on": True, "display_item": "", "item_model": ""}),
	"pap_machine": ElementDef(name="Pack-a-Punch", color="dark_red", particle=[0.8, 0.1, 0.1], particle_scale=1.0, has_rotation=True, egg_model="minecraft:creaking_spawn_egg", save_type="zb_object", save_path="pap_machines", emoji="🔥", defaults={"name": "Pack-a-Punch", "price": 5000, "power": True, "display_item": "", "item_model": ""}),
	"mystery_box_pos": ElementDef(name="Mystery Box Pos", color="light_purple", particle=[1.0, 0.0, 1.0], particle_scale=1.0, has_rotation=True, egg_model="minecraft:evoker_spawn_egg", save_type="zb_object", save_path="mystery_box.positions", emoji="📦", defaults={"can_start_on": True, "display_item": "", "item_model": ""}),
	"power_switch": ElementDef(name="Power Switch", color="green", particle=[0.0, 1.0, 0.0], particle_scale=1.0, has_rotation=True, egg_model="minecraft:slime_spawn_egg", save_type="zb_object", save_path="power_switch", emoji="⚡", defaults={}),
	"barrier": ElementDef(
		name="Barrier",
		color="aqua",
		particle=[0.0, 1.0, 1.0],
		particle_scale=1.0,
		has_rotation=True,
		egg_model="minecraft:guardian_spawn_egg",
		save_type="zb_object",
		save_path="barriers",
		emoji="🧱",
		defaults={
                                "block_enabled":  {"Name": "minecraft:oak_fence_gate", "Properties": {"open": "false"}},
                                "block_disabled": {"Name": "minecraft:oak_fence_gate", "Properties": {"open": "true"}},
                                "radius": 2,
                           },
	),
}

# Elements rendered as real in-game models in the editor (instead of dust particles).
# Each has a maps/editor/displays/<etype> function mirroring the game's own display setup,
# rebuilt every second so rotation/config edits on the marker stay in sync.
MODEL_DISPLAY_ELEMENTS: tuple[str, ...] = ("wallbuy", "perk_machine", "wunderfizz", "pap_machine", "mystery_box_pos", "power_switch", "barrier")

# Field documentation ───────────────────────────────────────────
# Tooltips shown (as a hover "ⓘ") next to constant/enum config fields in the element editor,
# so map makers don't have to guess what the magic numbers mean. Keyed by (element_type, field);
# a plain field-name key acts as a fallback shared across element types (e.g. "power").
FIELD_DOCS: dict[tuple[str, str] | str, str] = {
	("trap", "type"): "Trap behaviour:\n0 = Fire — lethal to zombies, burns players inside\n1 = Electric — lethal to zombies, shocks players inside\n2 = Turret — auto-fires at the nearest zombie every 5 ticks",
	("trap", "duration"): "How long the trap stays active, in ticks (20 ticks = 1 second).",
	("trap", "cooldown"): "Cooldown before the trap can be re-triggered, in ticks (20 = 1s).",
	("door", "animation"): "Open animation:\n0 = Destroy — block-break particles + sound\n1+ = Silent — blocks instantly replaced with air",
	("door", "link_id"): "Doors that share a link_id open together as a single purchase.",
	("door", "partial_price"): "Chip-in payments: points taken per right-click (0 = pay the full price at once).\nExample: price 5000 + partial_price 500 = 10 payments.\nDoor progress is GLOBAL — any mix of players can contribute, and the last\npayment is just whatever is left. Progress is shared by every linked door.",
	("perk_machine", "partial_price"): "Chip-in payments: points taken per right-click (0 = pay the full price at once).\nExample: price 2500 + partial_price 500 = 5 payments.\nPerk progress is LOCAL — each player pays down their own perk, nobody can\ncontribute to someone else's. Progress is lost when the perk is obtained.",
	("door", "back_group_id"): "Zombie spawn group_id unlocked behind this door (-1 = none).",
	("perk_machine", "name"): "Display label shown when hovering the machine.\nLeave EMPTY to auto-resolve the perk's canonical name from perk_id\n(e.g. juggernog -> Juggernog). Only set this to override that name.",
	("perk_machine", "perk_id"): _PERK_ID_DOC,
	("perk_machine", "price"): _PERK_PRICE_DOC,
	("wunderfizz", "all_perks"): "false = the machine only rolls perks that have a machine placed on\nthis map (like the Random Perk power-up).\ntrue = rolls across EVERY defined perk (BO2 Origins behaviour), so it\ncan grant perks with no machine on the map.",
	("wunderfizz", "price"): "Points per use. Cycles perk bottles and grants one random perk the\nbuyer doesn't already own, collectable by the buyer for 10s. Suggested: 1500.",
	("wallbuy", "weapon_id"): "Item id given on purchase. Guns (e.g. m1911, ak47, mp5),\nknives (bowie_knife, ~3000 pts), lethal grenades (frag_grenade,\nsemtex...), or tacticals (monkey_bomb). Non-guns route to their\nown slot: knife hotbar.0, lethals hotbar.7 (x4), tacticals hotbar.6 (x3).",
	("wallbuy", "magazine_id"): "Magazine item paired with the gun (e.g. m1911_mag).\nLeave empty for knife/grenade/tactical wallbuys.",
	("barrier", "radius"): "Block radius the barrier toggles open/closed around its marker.",
	"activation_box": "Optional [x, y, z, dx, dy, dz] box (relative to this spawn, in blocks).\nWhen set, this spawn only produces enemies while a player stands inside the box.\nx/y/z = corner offset from the spawn, dx/dy/dz = size. Empty [] = always active.",
	# Shared fallbacks (any element type):
	"can_start_on": "true = the machine is allowed to be the ACTIVE (usable) spot at game\nstart and after it roams. false = a valid roam destination, but never\nthe first active spot. Only one spot is active at a time; the rest show\na grayed-out disabled model. At least one spot must allow starting.",
	"power": "true = requires the map's power to be switched on before it works\nfalse = always usable",
	"price": "Cost in points to buy/use this element.",
}

# Mode Definitions ──────────────────────────────────────────────
@dataclass(frozen=True)
class EditorMode:
	""" One editor mode: its label and which elements map to which hotbar/inventory slots. """
	name: str
	color: str
	storage_key: str
	""" Key in {ns}:maps storage (multiplayer, zombies, missions). """
	slots: dict[str, str]


EDITOR_MODES: dict[str, EditorMode] = {
	"multiplayer": EditorMode(
		name="Multiplayer",
		color="gold",
		storage_key="multiplayer",
		slots={
			"base_coordinates": "hotbar.0",
			"red_spawn": "hotbar.1",
			"blue_spawn": "hotbar.2",
			"general_spawn": "hotbar.3",
			"out_of_bounds": "hotbar.4",
			"boundary": "hotbar.5",
			"search_and_destroy": "hotbar.6",
			"domination": "inventory.0",
			"hardpoint": "inventory.1",
			"start_command": "inventory.2",
			"respawn_command": "inventory.3",
		},
	),
	"zombies": EditorMode(
		name="Zombies",
		color="dark_green",
		storage_key="zombies",
		slots={
			"base_coordinates": "hotbar.0",
			"player_spawn_zb": "hotbar.1",
			"zombie_spawn": "hotbar.2",
			"wallbuy": "hotbar.3",
			"door": "hotbar.4",
			"trap": "hotbar.5",
			"perk_machine": "inventory.0",
			"mystery_box_pos": "inventory.1",
			"power_switch": "inventory.2",
			"out_of_bounds": "inventory.3",
			"boundary": "inventory.4",
			"pap_machine": "inventory.5",
			"start_command": "inventory.6",
			"special_spawn": "inventory.7",
			"barrier": "inventory.8",
			"wunderfizz": "inventory.9",
		},
	),
	"missions": EditorMode(
		name="Missions",
		color="aqua",
		storage_key="missions",
		slots={
			"base_coordinates": "hotbar.0",
			"mission_spawn": "hotbar.1",
			"enemy": "hotbar.2",
			"out_of_bounds": "hotbar.3",
			"boundary": "hotbar.4",
			"config": "hotbar.5",
			"start_command": "inventory.0",
			"respawn_command": "inventory.1",
		},
	),
}

MODE_LIST: list[str] = list(EDITOR_MODES.keys())
