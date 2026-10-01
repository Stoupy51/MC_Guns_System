""" The available-perk pool the random-perk power-up and Der Wunderfizz both roll against. """
# Imports
from stewbeet import Mem, write_versioned_function

from .definitions import PERK_DEFINITIONS


# Functions
def write_perk_pool() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Perk pool for the random-perk power-up and Der Wunderfizz: perks with a machine on this map (or all with #pool_all_perks)
	# that the pool_target player does not own. `mark` runs per placed machine at setup; flags clear at game start.
	perk_ids: list[str] = list(PERK_DEFINITIONS.keys())
	num_perks: int = len(perk_ids)

	## Macro: perk_id.
	write_versioned_function("zombies/perks/pool/mark", f"""
$scoreboard players set #map_perk_$(perk_id) {ns}.data 1
""")

	# #pool_chosen gets the index (-1 if none) and _pool.perk_id the perk; choose_iter walks the whole list at most once.
	write_versioned_function("zombies/perks/pool/choose", f"""
scoreboard players set #pool_chosen {ns}.data -1
data modify storage {ns}:temp _pool set value {{}}

# From a random index, walk until an available perk.
execute store result score #pool_roll {ns}.data run random value 0..{num_perks - 1}
scoreboard players set #pool_tries {ns}.data 0
function {ns}:v{version}/zombies/perks/pool/choose_iter
""")

	iter_lines: str = ""
	for i, perk_id in enumerate(perk_ids):
		iter_lines += f'execute if score #pool_roll {ns}.data matches {i} run function {ns}:v{version}/zombies/perks/pool/try_index {{perk_id:"{perk_id}"}}\n'
		iter_lines += f"execute if score #pool_chosen {ns}.data matches 0.. run return 0\n"
	write_versioned_function("zombies/perks/pool/choose_iter", f"""
# At most one full loop.
scoreboard players add #pool_tries {ns}.data 1
execute if score #pool_tries {ns}.data matches {num_perks + 1}.. run return 0
execute if score #pool_chosen {ns}.data matches 0.. run return 0

{iter_lines}
scoreboard players add #pool_roll {ns}.data 1
execute if score #pool_roll {ns}.data matches {num_perks}.. run scoreboard players set #pool_roll {ns}.data 0
function {ns}:v{version}/zombies/perks/pool/choose_iter
""")

	# Only called with the perk at #pool_roll.
	write_versioned_function("zombies/perks/pool/try_index", f"""
scoreboard players set #pool_slot {ns}.data 0
$execute if score #map_perk_$(perk_id) {ns}.data matches 1 run scoreboard players set #pool_slot {ns}.data 1
execute if score #pool_all_perks {ns}.data matches 1 run scoreboard players set #pool_slot {ns}.data 1
$execute if score @n[tag={ns}.pool_target] {ns}.zb.perk.$(perk_id) matches 1 run scoreboard players set #pool_slot {ns}.data 0
execute if score #pool_slot {ns}.data matches 1 run scoreboard players operation #pool_chosen {ns}.data = #pool_roll {ns}.data
$execute if score #pool_slot {ns}.data matches 1 run data modify storage {ns}:temp _pool.perk_id set value "$(perk_id)"
""")

