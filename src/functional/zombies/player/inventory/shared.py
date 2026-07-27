""" The custom-data predicate identifying what belongs in each managed slot. """
# Imports
from dataclasses import dataclass


# Classes
@dataclass(frozen=True)
class SlotPredicates:
	""" The custom-data predicate identifying what belongs in each managed zombies slot.

	Zombies pins every item to one slot, so a predicate doubles as the "is this the right item here"
	test and as the tag written back onto whatever gets moved into that slot.
	"""
	knife: str
	gun_1: str
	gun_2: str
	gun_3: str
	ability: str
	equipment_1: str
	equipment_2: str
	info: str
	mag_1: str
	mag_2: str
	mag_3: str

# Functions
def slot_predicates(ns: str) -> SlotPredicates:
	""" Build the slot predicates for a namespace.

	Args:
		ns (str): The project namespace.
	Returns:
		SlotPredicates: One `custom_data` predicate body per managed slot.

	Examples:
		>>> slot_predicates("mgs").knife
		'{mgs:{knife:true,zombies:{hotbar:0}}}'
	"""
	return SlotPredicates(
		knife=       "{" + ns + ":{knife:true,zombies:{hotbar:0}}}",
		gun_1=       "{" + ns + ":{gun:true,zombies:{hotbar:1}}}",
		gun_2=       "{" + ns + ":{gun:true,zombies:{hotbar:2}}}",
		gun_3=       "{" + ns + ":{gun:true,zombies:{hotbar:3}}}",
		ability=     "{" + ns + ":{zb_ability_item:true,zombies:{hotbar:4}}}",
		equipment_2= "{" + ns + ":{gun:true,zombies:{hotbar:6}}}",
		equipment_1= "{" + ns + ":{gun:true,zombies:{hotbar:7}}}",
		info=        "{" + ns + ":{zb_info:true,zombies:{hotbar:8}}}",
		mag_1=       "{" + ns + ":{magazine:true,zombies:{inventory:1}}}",
		mag_2=       "{" + ns + ":{magazine:true,zombies:{inventory:2}}}",
		mag_3=       "{" + ns + ":{magazine:true,zombies:{inventory:3}}}",
	)

