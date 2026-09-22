""" Preset multiplayer classes and the SNBT builders for their dialog rows. """
# Imports
from typing import ClassVar

from stewbeet import JsonDict

from ...config.catalogs import PERKS


# Classes
class MultiplayerClasses:
	""" Preset multiplayer classes and the SNBT builders for their dialog rows. """

	CONSUMABLE_MAGS: ClassVar[set[str]] = {"rpg7_rocket", "mosin_bullet", "m24_bullet", "spas12_shell", "m500_shell", "m590_shell", "element_115"}
	""" Consumable magazine item ids, where the stack count is the bullet count via the set_consumable_count modifier. """

	# Functions
	@staticmethod
	def make_slot_snbt(ns: str, slot: str, loot: str, count: int = 1, consumable: bool = False, bullets: int = 0) -> str:
		""" Build the SNBT string for a single loadout slot entry. """
		return f'{{slot:"{slot}",loot:"{ns}:i/{loot}",count:{count},consumable:{"1b" if consumable else "0b"},bullets:{bullets}}}'

	CLASSES: ClassVar[dict[str, JsonDict]] = {
		"assault": {
			"name": "Assault",
			"lore": "Versatile frontline",
			"main": {"gun": "ak47", "mag": "ak47_mag", "mag_count": 3},
			"secondary": {"gun": "m1911", "mag": "m1911_mag", "mag_count": 2},
			"equipment": {"frag_grenade": 2, "smoke_grenade": 1},
			"perks": ["quick_reload", "scavenger", "quick_swap"],
		},
		"rifleman": {
			"name": "Rifleman",
			"lore": "Accurate mid-range",
			"main": {"gun": "m16a4", "mag": "m16a4_mag", "mag_count": 3},
			"secondary": {"gun": "m9", "mag": "m9_mag", "mag_count": 2},
			"equipment": {"flash_grenade": 1, "smoke_grenade": 1},
			"perks": ["quick_reload", "tactical_mask", "tracker"],
		},
		"support": {
			"name": "Support",
			"lore": "Suppressive heavy",
			"main": {"gun": "m249", "mag": "m249_mag", "mag_count": 3},
			"secondary": {"gun": "glock17", "mag": "glock17_mag", "mag_count": 2},
			"equipment": {"smoke_grenade": 2},
			"perks": ["scavenger", "juggernaut", "flak_jacket"],
		},
		"sniper": {
			"name": "Sniper",
			"lore": "Long-range precision",
			"main": {"gun": "m24_4", "mag": "m24_bullet", "mag_count": 10},
			"secondary": {"gun": "deagle", "mag": "deagle_mag", "mag_count": 2},
			"equipment": {"flash_grenade": 1},
			"perks": ["quick_swap", "tracker", "tactical_mask"],
		},
		"smg": {
			"name": "SMG",
			"lore": "Close quarters",
			"main": {"gun": "mp7", "mag": "mp7_mag", "mag_count": 4},
			"secondary": {"gun": "glock18", "mag": "glock18_mag", "mag_count": 2},
			"equipment": {"flash_grenade": 2},
			"perks": ["quick_reload", "quick_swap", "quick_fix"],
		},
		"shotgunner": {
			"name": "Shotgunner",
			"lore": "Breaching / CQB",
			"main": {"gun": "spas12", "mag": "spas12_shell", "mag_count": 16},
			"secondary": {"gun": "m9", "mag": "m9_mag", "mag_count": 2},
			"equipment": {"semtex": 2},
			"perks": ["juggernaut", "flak_jacket", "quick_swap"],
		},
		"engineer": {
			"name": "Engineer",
			"lore": "Objective / demolitions",
			"main": {"gun": "mp5", "mag": "mp5_mag", "mag_count": 3},
			"secondary": {"gun": "makarov", "mag": "makarov_mag", "mag_count": 2},
			"equipment": {"semtex": 2, "smoke_grenade": 1},
			"perks": ["flak_jacket", "scavenger", "tactical_mask"],
		},
		"medic": {
			"name": "Medic",
			"lore": "Team sustain",
			"main": {"gun": "famas", "mag": "famas_mag", "mag_count": 3},
			"secondary": {"gun": "m1911", "mag": "m1911_mag", "mag_count": 2},
			"equipment": {"smoke_grenade": 2},
			"perks": ["quick_fix", "tactical_mask", "scavenger"],
		},
		"marksman": {
			"name": "Marksman",
			"lore": "Semi-auto precision",
			"main": {"gun": "svd", "mag": "svd_mag", "mag_count": 3},
			"secondary": {"gun": "glock17", "mag": "glock17_mag", "mag_count": 2},
			"equipment": {"flash_grenade": 1, "smoke_grenade": 1},
			"perks": ["quick_reload", "tracker", "tactical_mask"],
		},
		"heavy": {
			"name": "Heavy",
			"lore": "Armored suppressor",
			"main": {"gun": "rpk", "mag": "rpk_mag", "mag_count": 3},
			"secondary": {"gun": "makarov", "mag": "makarov_mag", "mag_count": 2},
			"equipment": {"frag_grenade": 2},
			"perks": ["juggernaut", "flak_jacket", "scavenger"],
		},
	}
	""" Balanced team-vs-team class loadouts, used at build time to generate the SNBT that initialises storage. """

	PERK_NAMES: ClassVar[dict[str, str]] = {perk.perk_id: perk.display_name for perk in PERKS}
	""" perk_id to display name, from the shared PERKS catalog. """

	CLASS_IDS: ClassVar[dict[str, int]] = {class_id: idx + 1 for idx, class_id in enumerate(CLASSES)}
	""" Class number assignments, 1-indexed, used for the scoreboard mgs.mp.class. """

	EQUIP_LABELS: ClassVar[dict[str, str]] = {
		"frag_grenade": "Frag", "semtex": "Semtex",
		"flash_grenade": "Flash", "smoke_grenade": "Smoke",
	}
	""" Short grenade names for a class's equipment line, falling back on the item id. """

	TRIGGER_OFFSET: int = 10
	""" trigger_value = TRIGGER_OFFSET + class_num. Must match the dispatch formula in player_config.py (10 + class_num, so 11..20). """

	@staticmethod
	def get_class_description(class_id: str) -> str:
		""" Get the hover/lore description text for a class. """
		data = MultiplayerClasses.CLASSES[class_id]
		main_gun: str = data["main"]["gun"].upper().replace("_", " ")
		secondary_gun: str = data.get("secondary", {}).get("gun", "").upper().replace("_", " ")
		return f"{data['lore']}\nMain: {main_gun}\nSecondary: {secondary_gun}"

	@staticmethod
	def build_class_snbt(ns: str, class_id: str, class_data: JsonDict, class_num: int) -> str:
		""" Build the SNBT representation of a class for storage initialization.
		The format is designed for dynamic loadout application via recursive slot iteration. """
		trigger_value: int = MultiplayerClasses.TRIGGER_OFFSET + class_num
		main_gun: str = class_data["main"]["gun"]
		secondary_gun: str = class_data.get("secondary", {}).get("gun", "")
		equipment: dict[str, int] = class_data.get("equipment", {})
		make_slot = MultiplayerClasses.make_slot_snbt

		# Primary on hotbar.1 (hotbar.0 is reserved for the knife, given in apply_class_dynamic), secondary on hotbar.2,
		# grenades from hotbar.8 downwards, then magazines from inventory.0 on
		slots: list[str] = [make_slot(ns, "hotbar.1", main_gun)]
		if secondary_gun:
			slots.append(make_slot(ns, "hotbar.2", secondary_gun))
		slots += [make_slot(ns, f"hotbar.{8 - index}", item_id, count=count) for index, (item_id, count) in enumerate(equipment.items())]
		main_mags: list[str] = MultiplayerClasses.magazine_slots(ns, class_data["main"], first_slot=0)
		slots += main_mags
		if "secondary" in class_data:
			slots += MultiplayerClasses.magazine_slots(ns, class_data["secondary"], first_slot=len(main_mags))
		slots_snbt: str = ",".join(slots)

		# Equipment display string, ex: "2x Frag, 1x Smoke"
		equip_parts: list[str] = [f"{count}x {MultiplayerClasses.EQUIP_LABELS.get(item_id, item_id)}" for item_id, count in equipment.items()]
		equip_display: str = ", ".join(equip_parts) if equip_parts else "None"

		main_mag_count: int = class_data["main"].get("mag_count", 0)
		secondary_mag_count: int = class_data.get("secondary", {}).get("mag_count", 0)

		# Perks: stored as a string list (matches custom loadout format) + a display string
		perks: list[str] = class_data.get("perks", [])
		perks_snbt: str = ",".join(f'"{perk_id}"' for perk_id in perks)
		perks_display: str = ", ".join(MultiplayerClasses.PERK_NAMES.get(perk_id, perk_id) for perk_id in perks) if perks else "None"

		return (
			f'{{id:"{class_id}",name:"{class_data["name"]}",lore:"{class_data["lore"]}",'
			f'trigger_value:{trigger_value},main_gun:"{main_gun}",secondary_gun:"{secondary_gun}",'
			f'main_mag_count:{main_mag_count},secondary_mag_count:{secondary_mag_count},'
			f'equip_display:"{equip_display}",perks_display:"{perks_display}",'
			f'perks:[{perks_snbt}],'
			f'slots:[{slots_snbt}]}}'
		)

	@staticmethod
	def magazine_slots(ns: str, weapon: JsonDict, first_slot: int) -> list[str]:
		""" Inventory slots holding a weapon's magazines, from `inventory.<first_slot>` on.

		A consumable magazine is one stack whose count is the bullet count; any other takes one slot per magazine.

		Args:
			weapon: A class's `main` or `secondary` entry, reading `mag` and `mag_count`.
		"""
		mag_id: str = weapon["mag"]
		mag_count: int = weapon.get("mag_count", 0)
		if mag_id in MultiplayerClasses.CONSUMABLE_MAGS:
			return [MultiplayerClasses.make_slot_snbt(ns, f"inventory.{first_slot}", mag_id, consumable=True, bullets=mag_count)]
		return [MultiplayerClasses.make_slot_snbt(ns, f"inventory.{first_slot + index}", mag_id) for index in range(mag_count)]

