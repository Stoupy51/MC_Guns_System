""" Save slots: a run taken out of the world between two rounds, and put back later on the same map.

A slot of `mgs:zombies_saves slots[]` is empty (`{}`) or written by save/capture, read by save/restore:
{format, pack, name, map_id, variant, round, saved_at, players:[{uuid, scores:{...}, inventory:[...]}],
map:{power, opened:[link ids], doors:[{id, paid}], barricades:[{id, state}], traps:[{id, cd}], box, box_pulls, box_dry_ray_gun, wunderfizz, wunderfizz_uses}}
"""
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .capture import write_save_capture
from .menus import write_save_menus
from .restore import write_save_restore

# Constants
SLOT_COUNT: int = 5


# Functions
def generate_zombies_save() -> None:
	ns: str = Mem.ctx.project_id
	empty_slots: str = ",".join("{}" for _ in range(SLOT_COUNT))
	write_load_file(f"execute unless data storage {ns}:zombies_saves slots[{SLOT_COUNT - 1}] run data modify storage {ns}:zombies_saves slots set value [{empty_slots}]")

	write_versioned_function("zombies/save/delete", f"""
$data modify storage {ns}:zombies_saves slots[$(slot)] set value {{}}
function {ns}:v{Mem.ctx.project_version}/zombies/save/load_menu
""")

	write_save_capture()
	write_save_restore()
	write_save_menus(SLOT_COUNT)

