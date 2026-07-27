""" The perk tooltip line and the two row builders both browsers share. """
# Imports

from ..catalogs import PERKS

# Constants
PERK_CONCAT: str = "".join(f"$(perk{i})" for i in range(len(PERKS)))
""" Concatenation of every perk slot, so a tooltip shows all chosen perks and nothing for the rest. """

# Functions
def normalize_btn_fields(ns: str) -> str:
	""" Return the lines filling in every optional _btn_data field a row tooltip reads.

	A loadout saved before a field existed simply has no value for it, and a macro substituting a
	missing key fails the whole command, so each one is defaulted before the row is built.

	Args:
		ns (str): The project namespace.
	Returns:
		str: One command per line, ready to embed in a function body.
	"""
	# Perk display lines for tooltips: \\n in SNBT is stored as \n (backslash + n, 2 chars), which macro substitution turns back into a newline
	perk_disp: str = (
		"\n".join(f"data modify storage {ns}:temp _btn_data.perk{i} set value \"\"" for i in range(len(PERKS)))
		+ "\n"
		+ "\n".join(
			f'execute if data storage {ns}:temp _btn_data{{perks:["{p.perk_id}"]}} run data modify storage {ns}:temp _btn_data.perk{i} set value "\\\\n- {p.display_name}"'
			for i, p in enumerate(PERKS)
		)
	)
	return "\n".join([
		f'execute unless data storage {ns}:temp _btn_data.perks run data modify storage {ns}:temp _btn_data.perks set value []',
		f'execute store result storage {ns}:temp _btn_data.perks_count int 1 run data get storage {ns}:temp _btn_data.perks',
		perk_disp,
		f'execute unless data storage {ns}:temp _btn_data.points_used run data modify storage {ns}:temp _btn_data.points_used set value 0',
		f'execute unless data storage {ns}:temp _btn_data.favorites_count run data modify storage {ns}:temp _btn_data.favorites_count set value 0',
		f'execute unless data storage {ns}:temp _btn_data.likes run data modify storage {ns}:temp _btn_data.likes set value 0',
		f'execute unless data storage {ns}:temp _btn_data.primary_mag_count run data modify storage {ns}:temp _btn_data.primary_mag_count set value 1',
		f'execute unless data storage {ns}:temp _btn_data.secondary_mag_count run data modify storage {ns}:temp _btn_data.secondary_mag_count set value 0',
		f'execute unless data storage {ns}:temp _btn_data.equip_slot1_name run data modify storage {ns}:temp _btn_data.equip_slot1_name set value "?"',
		f'execute unless data storage {ns}:temp _btn_data.equip_slot2_name run data modify storage {ns}:temp _btn_data.equip_slot2_name set value "?"',
		f'execute unless data storage {ns}:temp _btn_data.main_gun_display run data modify storage {ns}:temp _btn_data.main_gun_display set from storage {ns}:temp _btn_data.main_gun',
		f'execute unless data storage {ns}:temp _btn_data.secondary_gun_display run data modify storage {ns}:temp _btn_data.secondary_gun_display set value "None"',
	])

def compute_trig(ns: str, field: str, base: int) -> str:
	""" Return the lines storing `base + the current row's loadout id` into a _btn_data field.

	Args:
		ns (str):    The project namespace.
		field (str): The _btn_data key the trigger value lands in.
		base (int):  The first trigger value of the block reserved for this action.
	Returns:
		str: Three commands, one per line.
	"""
	return (
		f"execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id\n"
		f"scoreboard players add #trig {ns}.data {base}\n"
		f"execute store result storage {ns}:temp _btn_data.{field} int 1 run scoreboard players get #trig {ns}.data"
	)

