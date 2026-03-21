
# Shared command builders for zombies modules.
from ...config.catalogs import PRIMARY_WEAPONS, SECONDARY_WEAPONS
from ..helpers import MGS_TAG
from ..multiplayer.classes import CONSUMABLE_MAGS


def game_active_guard_cmd(ns: str) -> str:
	""" Return the standard guard command for active zombies games. """
	return f'execute unless data storage {ns}:zombies game{{state:"active"}} run return fail'


def deny_not_enough_points_body(ns: str, version: str, price_score: str) -> str:
	""" Standardized not-enough-points response body. """
	return f"""
tellraw @s [{MGS_TAG},{{"text":"You don't have enough points (","color":"red"}},{{"score":{{"name":"{price_score}","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" needed).","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""".strip()


def deny_requires_power_body(ns: str, version: str, label: str) -> str:
	""" Standardized requires-power response body. """
	return f"""
tellraw @s [{MGS_TAG},{{"text":"This {label} requires power.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""".strip()


def build_weapon_magazine_data() -> dict[str, tuple[str, int, bool]]:
	""" Build a mapping of weapon_id -> (magazine_id, magazine_count, is_consumable). """
	weapon_mag_data: dict[str, tuple[str, int, bool]] = {}

	# Process PRIMARY_WEAPONS: (item_id, display_name, category, magazine_id, default_mag_count)
	for weapon_id, _, _, mag_id, mag_count in PRIMARY_WEAPONS:
		is_consumable = mag_id in CONSUMABLE_MAGS
		weapon_mag_data[weapon_id] = (mag_id, mag_count, is_consumable)

	# Process SECONDARY_WEAPONS: (item_id, display_name, magazine_id, default_mag_count)
	for weapon_id, _, mag_id, mag_count in SECONDARY_WEAPONS:
		is_consumable = mag_id in CONSUMABLE_MAGS
		weapon_mag_data[weapon_id] = (mag_id, mag_count, is_consumable)

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

