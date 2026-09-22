""" Item definition setup: registers every item, then derives names, lore and components. """
# Imports
import json

import stouputils as stp
from stewbeet import (
	Context,
	Item,
	JsonDict,
	Mem,
	TextComponent,
	add_item_model_component,
	add_item_name_and_lore_if_missing,
	add_private_custom_data_for_namespace,
	add_smithed_ignore_vanilla_behaviours_convention,
	create_gradient_text as new_hex,
	set_manual_components,
)

from .config.catalogs import (
	GRENADE_TYPES,
	PRIMARY_WEAPONS,
	SCOPE_NAMES,
	SECONDARY_WEAPONS,
)
from .config.stats.colors import END_HEX, START_HEX
from .config.stats.keys import (
	CAPACITY,
	CASING_MODEL,
	COOLDOWN,
	DAMAGE,
	DECAY,
	EXPLOSION_DAMAGE,
	EXPLOSION_RADIUS,
	GRENADE_FUSE,
	GRENADE_TYPE,
	MODELS,
	PELLET_COUNT,
	RELOAD_TIME,
	REMAINING_BULLETS,
	SPEED_MULTIPLY_BASE,
	SWITCH,
)
from .database.camo import main as camo_main
from .database.items import main as main_items

# Constants
EMPTY_LORE_LINE: JsonDict = {"text": "", "italic": False}
""" Blank lore separator. NOT a bare "": that is a StringTag while the styled stat lines are
CompoundTags, and NBT lists are homogeneous, so the mix makes NbtOps wrap every line as
{"": <line>}, which zombies/pap re-parses and renders blank. A style keeps it a CompoundTag. """

WEAPON_NAMES: dict[str, str] = {w.item_id: w.display_name for w in (*PRIMARY_WEAPONS, *SECONDARY_WEAPONS)}
""" Catalog display name of every primary and secondary weapon, by item id. """

GRENADE_NAMES: dict[str, str] = {g.item_id: g.display_name for g in GRENADE_TYPES if g.item_id}
""" Catalog display name of every grenade, by item id. """

SCOPE_SUFFIXES: tuple[str, ...] = ("_1", "_2", "_3", "_4")
""" Item id suffixes of the scoped variants, keys of `SCOPE_NAMES`. """

# Functions
@stp.measure_time(printer=stp.progress, message="Set up item definitions")
def beet_default(ctx: Context) -> None:
	ns: str = ctx.project_id

	# Registration order matters
	main_items()
	add_class_menu(ns)

	for item in Mem.definitions:
		obj = Item.from_id(item)
		obj.components["custom_data"] = json.loads(json.dumps(obj.components.get("custom_data", {})))
		ns_data: JsonDict = obj.components["custom_data"].get(ns, {})
		if ns_data.get("gun"):
			setup_gun(ns, item, obj, ns_data.get("stats", {}))
		if ns_data.get("magazine"):
			stats: JsonDict = ns_data["stats"]
			obj.components["lore"] = [
				[*new_hex("Ammo Remaining ➤ ", START_HEX, END_HEX), str(stats[REMAINING_BULLETS]), {"text": "/", "color": f"#{END_HEX}"}, str(stats[CAPACITY])],
			]

	# Camo variants per weapon
	camo_main()

	# Zoom models sort to the end, and stay out of the give_all chests with the empty magazines
	Mem.definitions = dict(sorted(Mem.definitions.items(), key=lambda entry: sort_rank(ns, entry[0])))
	for item in Mem.definitions:
		if item.endswith(("_zoom", "_mag_empty")):
			Item.from_id(item).skip_gives = True

	# Final adjustments, keep them
	add_item_model_component(black_list=["item_ids","you_don't_want","in_that","list"])
	add_item_name_and_lore_if_missing()
	add_private_custom_data_for_namespace()		# Add a custom namespace for easy item detection
	add_smithed_ignore_vanilla_behaviours_convention()	# Smithed items convention
	set_manual_components(white_list=["item_name", "lore", "custom_name", "damage", "max_damage"]) # Components to include in the manual when hovering items (here is the default list)


def add_class_menu(ns: str) -> None:
	""" Register the multiplayer class menu item. """
	Item(
		id="class_menu",
		base_item="minecraft:warped_fungus_on_a_stick",
		components={
			"max_stack_size": 1,
			"custom_data": {ns: {"class_menu": True}},
			"rarity": "common",
			"item_name": [{"text": "Class Menu", "color": "gold", "italic": False}],
			"item_model": "minecraft:nether_star",
		},
	)


def setup_gun(ns: str, item: str, obj: Item, gun_stats: JsonDict) -> None:
	""" Fill in a gun's derived stats, name, lore and right-click components.

	Args:
		item:      Item id, possibly with a scope suffix and a `_zoom` suffix.
		gun_stats: The item's `stats` custom data, edited in place.
	"""
	base_name: str = item.replace("_zoom", "")
	scope_suffix: str = next((suffix for suffix in SCOPE_SUFFIXES if base_name.endswith(suffix)), "")

	display_name: str | None = gun_display_name(base_name.removesuffix(scope_suffix), gun_stats)
	if display_name:
		scope_name: str | None = SCOPE_NAMES.get(scope_suffix)
		if scope_suffix and scope_name:
			display_name = f"{display_name} ({scope_name})"
		obj.components["item_name"] = [{"text": display_name, "color": "gold", "italic": False}]

	if CASING_MODEL in gun_stats:
		gun_stats[CASING_MODEL] = f"{ns}:{gun_stats[CASING_MODEL]}"
	gun_stats[MODELS] = {"normal": f"{ns}:{base_name}", "zoom": f"{ns}:{base_name}_zoom"}

	# Start with a full magazine
	gun_stats[REMAINING_BULLETS] = gun_stats[CAPACITY]

	# _3 variants get x3 zoom, _4 variants x4
	if scope_suffix in ("_3", "_4"):
		gun_stats["scope_level"] = int(scope_suffix[1])

	# consumable + use_effects give tick-perfect right-click detection
	obj.components["consumable"] = {
		"consume_seconds": 1_000_000,  # Very high value to avoid actual consumption
		"animation": "spear",   # Not "none" because of "use" animation still present, but "spear" has minimal animation
		"sound": "minecraft:intentionally_empty",
		"has_consume_particles": False
	}
	obj.components["use_effects"] = {
		"can_sprint": True,
		"speed_multiplier": 1.0,
		"interact_vibrations": False
	}
	obj.components["food"] = {"saturation":0,"nutrition":0,"can_always_eat":True}

	# Held-weapon movement penalty
	if SPEED_MULTIPLY_BASE in gun_stats:
		attribute_modifiers: list[JsonDict] = obj.components.setdefault("attribute_modifiers", [])
		attribute_modifiers.append({
			"type": "movement_speed",
			"amount": gun_stats[SPEED_MULTIPLY_BASE],
			"operation": "add_multiplied_base",
			"slot": "mainhand",
			"id": f"{ns}:weapon_weight_speed",
		})

	# Grenades get their own lore, and stack
	if GRENADE_TYPE in gun_stats:
		obj.components["max_stack_size"] = 16
		obj.components["lore"] = grenade_lore(gun_stats)
	else:
		obj.components["lore"] = gun_lore(gun_stats)


def gun_display_name(base_weapon_id: str, gun_stats: JsonDict) -> str | None:
	""" Catalog name of a gun or grenade, falling back on its grenade type.

	Args:
		base_weapon_id: Item id without its scope and `_zoom` suffixes.
	Returns:
		The display name, None when neither the catalog nor a grenade type names it.
	"""
	display_name: str | None = WEAPON_NAMES.get(base_weapon_id) or GRENADE_NAMES.get(base_weapon_id)
	if display_name or GRENADE_TYPE not in gun_stats:
		return display_name
	grenade_key: str = str(gun_stats[GRENADE_TYPE])
	return GRENADE_NAMES.get(grenade_key) or GRENADE_NAMES.get(f"{grenade_key}_grenade") or grenade_key.replace("_", " ").title()


def gun_lore(gun_stats: JsonDict) -> list[TextComponent]:
	""" Stat lines of a firearm, with fire rate and pellet count only when the gun has them. """
	fire_rate_component: list[TextComponent] = []
	if COOLDOWN in gun_stats:
		fire_rate: float = 20 / gun_stats[COOLDOWN]
		fire_rate_unit: str = "shots/s" if fire_rate > 1.0 else "s/shot"
		fire_rate_component.append([*new_hex("Fire Rate             ➤ ", START_HEX, END_HEX), f"{fire_rate:.1f} ", *new_hex(fire_rate_unit, END_HEX, START_HEX, text_length=10)])

	pellet_component: list[TextComponent] = []
	if PELLET_COUNT in gun_stats:
		pellet_component.append([*new_hex("Pellets Per Shot    ➤ ", START_HEX, END_HEX), str(gun_stats[PELLET_COUNT])])

	return [
		[*new_hex("Damage Per Bullet  ➤ ", START_HEX, END_HEX),    str(gun_stats[DAMAGE])],
		[*new_hex("Ammo Remaining      ➤ ", START_HEX, END_HEX),   str(gun_stats[REMAINING_BULLETS]),      {"text":"/","color":f"#{END_HEX}"}, str(gun_stats[CAPACITY])],
		[*new_hex("Reloading Time       ➤ ", START_HEX, END_HEX),  f"{gun_stats[RELOAD_TIME] / 20:.1f}",   {"text":"s","color":f"#{END_HEX}"}],
		*fire_rate_component,
		*pellet_component,
		[*new_hex("Damage Decay       ➤ ", START_HEX, END_HEX),    f"{gun_stats[DECAY] * 100:.0f}",        {"text":"%","color":f"#{END_HEX}"}],
		[*new_hex("Switch Time           ➤ ", START_HEX, END_HEX), f"{gun_stats[SWITCH] / 20:.1f}",        {"text":"s","color":f"#{END_HEX}"}],
		EMPTY_LORE_LINE,
	]


def grenade_lore(gun_stats: JsonDict) -> list[TextComponent]:
	""" Stat lines of a grenade, with explosion damage and radius only when it has them. """
	fuse_seconds: float = gun_stats.get(GRENADE_FUSE, 0) / 20
	lore: list[TextComponent] = [
		[*new_hex("Type                  ➤ ", START_HEX, END_HEX), gun_stats[GRENADE_TYPE].replace("_", " ").title()],
		[*new_hex("Fuse Time            ➤ ", START_HEX, END_HEX), f"{fuse_seconds:.1f}", {"text":"s","color":f"#{END_HEX}"}],
	]
	if EXPLOSION_DAMAGE in gun_stats:
		lore.insert(-1,
			[*new_hex("Explosion Damage  ➤ ", START_HEX, END_HEX), str(gun_stats[EXPLOSION_DAMAGE])]
		)
	if EXPLOSION_RADIUS in gun_stats:
		lore.insert(-1,
			[*new_hex("Explosion Radius   ➤ ", START_HEX, END_HEX), str(gun_stats[EXPLOSION_RADIUS])," ",{"text":"blocks","color":f"#{END_HEX}"}]
		)
	return [*lore, EMPTY_LORE_LINE]


def sort_rank(ns: str, item_id: str) -> int:
	""" Position group of an item in the definitions: plain items, empty magazines, zoom models, then casings. """
	if Item.from_id(item_id).components.get("custom_data", {}).get(ns, {}).get("casing"):
		return 4
	if item_id.endswith("_zoom"):
		return 2
	if item_id.endswith("_mag_empty"):
		return 1
	return 0

