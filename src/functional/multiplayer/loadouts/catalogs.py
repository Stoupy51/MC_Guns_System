
# Imports
from ....config.catalogs import *
from ..classes import CONSUMABLE_MAGS


def build_custom_loadout_slots_snbt(ns: str, primary_id: str, secondary_id: str, equipment_preset_idx: int) -> str:
	""" Build the slots SNBT array from weapon choices (same format as default class slots).
	Returns the SNBT string for the slots array content (without outer brackets).
	LEGACY: used for default classes only. Custom loadouts use build_custom_loadout_slots_new """
	slots: list[str] = []

	def add_slot(slot: str, loot: str, count: int = 1, consumable: bool = False, bullets: int = 0) -> None:
		slots.append(
			f'{{slot:"{slot}",loot:"{ns}:i/{loot}",count:{count},consumable:{"1b" if consumable else "0b"},bullets:{bullets}}}'
		)

	# Primary weapon → hotbar.0
	primary = PRIMARY_WEAPONS[PRIMARY_INDEX[primary_id]]
	add_slot("hotbar.0", primary[0])

	# Secondary weapon → hotbar.1 (if selected)
	secondary = SECONDARY_WEAPONS[SECONDARY_INDEX[secondary_id]] if secondary_id else None
	if secondary:
		add_slot("hotbar.1", secondary[0])

	# Equipment → hotbar.8, hotbar.7, ...
	preset = EQUIPMENT_PRESETS[equipment_preset_idx]
	equip_slot = 8
	for item_id, count in preset[2].items():
		add_slot(f"hotbar.{equip_slot}", item_id, count=count)
		equip_slot -= 1

	# Primary magazines → inventory.0, inventory.1, ...
	inv_slot = 0
	mag_id = primary[3]
	mag_count = primary[4]
	if mag_id in CONSUMABLE_MAGS:
		add_slot(f"inventory.{inv_slot}", mag_id, consumable=True, bullets=mag_count)
		inv_slot += 1
	else:
		for _ in range(mag_count):
			add_slot(f"inventory.{inv_slot}", mag_id)
			inv_slot += 1

	# Secondary magazines → continuing inventory slots
	if secondary:
		sec_mag_id = secondary[2]
		sec_mag_count = secondary[3]
		if sec_mag_id in CONSUMABLE_MAGS:
			add_slot(f"inventory.{inv_slot}", sec_mag_id, consumable=True, bullets=sec_mag_count)
			inv_slot += 1
		else:
			for _ in range(sec_mag_count):
				add_slot(f"inventory.{inv_slot}", sec_mag_id)
				inv_slot += 1

	return ",".join(slots)


def build_custom_loadout_slots_pick10(
	ns: str,
	primary_full: str,
	primary_mag_id: str,
	primary_mag_count: int,
	secondary_full: str,
	secondary_mag_id: str,
	secondary_mag_count: int,
	equip_slot1: str,
	equip_slot2: str,
) -> str:
	""" Build the slots SNBT for a Pick-10 custom loadout.
	primary_full / secondary_full are the scope-modified IDs (e.g. 'ak47_3').
	mag counts are chosen by player. equip_slot1/2 are item IDs or '' for none """
	slots: list[str] = []
	inv_slot = 0

	def add_slot(slot: str, loot: str, count: int = 1, consumable: bool = False, bullets: int = 0) -> None:
		slots.append(
			f'{{slot:"{slot}",loot:"{ns}:i/{loot}",count:{count},consumable:{"1b" if consumable else "0b"},bullets:{bullets}}}'
		)

	# Primary weapon → hotbar.0
	add_slot("hotbar.0", primary_full)

	# Secondary weapon → hotbar.1 (if selected)
	if secondary_full:
		add_slot("hotbar.1", secondary_full)

	# Equipment slots → hotbar.8 first, then hotbar.7
	equip_hotbar = 8
	if equip_slot1:
		add_slot(f"hotbar.{equip_hotbar}", equip_slot1, count=1)
		equip_hotbar -= 1
	if equip_slot2:
		add_slot(f"hotbar.{equip_hotbar}", equip_slot2, count=1)

	# Primary magazines → inventory.0, inventory.1, ...
	if primary_mag_id in CONSUMABLE_MAGS:
		# Consumable: 1 slot with count = bullets per stack (default from primary data)
		primary_base = primary_full.rstrip("_1234")
		if primary_base in PRIMARY_INDEX:
			bullets = PRIMARY_WEAPONS[PRIMARY_INDEX[primary_base]][4]
		else:
			bullets = PRIMARY_WEAPONS[PRIMARY_INDEX[primary_full]][4]
		add_slot(f"inventory.{inv_slot}", primary_mag_id, consumable=True, bullets=bullets)
		inv_slot += 1
	else:
		for _ in range(primary_mag_count):
			add_slot(f"inventory.{inv_slot}", primary_mag_id)
			inv_slot += 1

	# Secondary magazines → continuing inventory slots
	if secondary_full and secondary_mag_id:
		if secondary_mag_id in CONSUMABLE_MAGS:
			secondary_base = secondary_full.rstrip("_1234")
			if secondary_base in SECONDARY_INDEX:
				bullets = SECONDARY_WEAPONS[SECONDARY_INDEX[secondary_base]][3]
			else:
				bullets = SECONDARY_WEAPONS[SECONDARY_INDEX[secondary_full]][3]
			add_slot(f"inventory.{inv_slot}", secondary_mag_id, consumable=True, bullets=bullets)
			inv_slot += 1
		else:
			for _ in range(secondary_mag_count):
				add_slot(f"inventory.{inv_slot}", secondary_mag_id)
				inv_slot += 1

	return ",".join(slots)

