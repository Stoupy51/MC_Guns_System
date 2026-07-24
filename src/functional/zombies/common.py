
# Shared command builders for zombies modules.
from stewbeet import write_versioned_function

from ...config.catalogs import PRIMARY_WEAPONS, SECONDARY_WEAPONS
from ..core.feedback import zb_sound
from ..helpers import MGS_TAG, game_active_guard
from ..multiplayer.classes import CONSUMABLE_MAGS


def game_active_guard_cmd(ns: str) -> str:
	""" Return the standard guard command for active zombies games. """
	return game_active_guard(ns, "zombies")


def write_deny_functions() -> None:
	""" The two handlers every "you can't do that" path in zombies falls back to. """
	# The message rides in as a whole text component so the English stays a literal here for
	# auto.lang_file. The argument is `msg`, not `text`, or lang_file would translate the outer
	# quoted value instead of the component inside it.
	write_versioned_function("zombies/deny/message", f"""
$tellraw @s [{MGS_TAG},$(msg)]
{zb_sound('deny')}
""")

	# Same message everywhere, only the score holding the price differs
	write_versioned_function("zombies/deny/not_enough_points", f"""
$tellraw @s [{MGS_TAG},{{"text":"You don't have enough points (","color":"red"}},{{"score":{{"name":"$(score)","objective":"$(obj)"}},"color":"yellow"}},{{"text":" needed).","color":"red"}}]
{zb_sound('deny')}
""")


def deny_cmd(ns: str, version: str, component: str) -> str:
	""" One command showing `component` in chat with the deny sound, so it survives `return run`. """
	return f"function {ns}:v{version}/zombies/deny/message {{msg:'{component}'}}"


def deny_not_enough_points_cmd(ns: str, version: str, price_score: str, objective: str = "") -> str:
	""" One command for the shared not-enough-points message, naming the score that holds the price. """
	obj: str = objective or f"{ns}.data"
	return f'function {ns}:v{version}/zombies/deny/not_enough_points {{score:"{price_score}",obj:"{obj}"}}'


def build_weapon_magazine_data() -> dict[str, tuple[str, int, bool]]:
	""" Build a mapping of weapon_id -> (magazine_id, magazine_count, is_consumable). """
	weapon_mag_data: dict[str, tuple[str, int, bool]] = {}

	# Process PRIMARY_WEAPONS
	for w in PRIMARY_WEAPONS:
		is_consumable = w.magazine_id in CONSUMABLE_MAGS
		weapon_mag_data[w.item_id] = (w.magazine_id, w.default_mag_count, is_consumable)

	# Process SECONDARY_WEAPONS
	for w in SECONDARY_WEAPONS:
		is_consumable = w.magazine_id in CONSUMABLE_MAGS
		weapon_mag_data[w.item_id] = (w.magazine_id, w.default_mag_count, is_consumable)

	return weapon_mag_data


def get_weapon_magazine_info(weapon_id: str, weapon_mag_data: dict[str, tuple[str, int, bool]] | None = None) -> tuple[str, int, bool]:
	""" Lookup magazine info for a specific weapon.

	Args:
		weapon_id: The weapon to look up
		weapon_mag_data: Optional pre-built data (builds if not provided)

	Returns:
		Tuple of (magazine_id, magazine_count, is_consumable)
	"""
	if weapon_mag_data is None:
		weapon_mag_data = build_weapon_magazine_data()
	if weapon_id not in weapon_mag_data:
		raise ValueError(f"Unknown weapon_id: {weapon_id}")
	return weapon_mag_data[weapon_id]


def give_magazine_for_weapon_cmd(
	ns: str, version: str, inventory_slot: str, weapon_id: str,
	weapon_mag_data: dict[str, tuple[str, int, bool]] | None = None
) -> str:
	""" Generate command to give the default magazine for a weapon to inventory slot.

	Args:
		ns: Namespace
		version: Project version
		inventory_slot: Target inventory slot (e.g., "inventory.1")
		weapon_id: The weapon_id to get magazine for
		weapon_mag_data: Optional pre-built weapon magazine data (builds if not provided)

	Returns:
		Minecraft command (macro-compatible) to give the magazine
	"""
	if weapon_mag_data is None:
		weapon_mag_data = build_weapon_magazine_data()
	if weapon_id not in weapon_mag_data:
		raise ValueError(f"Unknown weapon_id: {weapon_id}")
	mag_id, mag_count, is_consumable = weapon_mag_data[weapon_id]

	# Generate appropriate command based on magazine type
	if is_consumable:
		# Consumable: give item, set bullet count via modifier
		return f"""scoreboard players set #bullets {ns}.data {mag_count}
loot replace entity @s {inventory_slot} loot {ns}:i/{mag_id}
item modify entity @s {inventory_slot} {ns}:v{version}/set_consumable_count"""
	else:
		# Regular magazine: loot replace directly (already has bullets set in item definition)
		return f"loot replace entity @s {inventory_slot} loot {ns}:i/{mag_id}"


def give_magazine_pool_entries(ns: str, version: str, weapon_mag_data: dict[str, tuple[str, int, bool]] | None = None) -> str:
	"""Generate pool entries for mystery box / dynamic weapon selection with magazine metadata.

	Returns SNBT array entries with weapon_id, mag_id, mag_count, and consumable flag.
	"""
	if weapon_mag_data is None:
		weapon_mag_data = build_weapon_magazine_data()

	entries: list[str] = []
	for weapon_id, (mag_id, mag_count, is_consumable) in weapon_mag_data.items():
		consumable_flag = "1b" if is_consumable else "0b"
		entry = (
			f'{{weapon_id:"{weapon_id}",'
			f'mag_id:"{mag_id}",'
			f'mag_count:{mag_count},'
			f'consumable:{consumable_flag}}}'
		)
		entries.append(entry)

	return ",".join(entries)

