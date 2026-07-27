""" Scores and storage the active perk effects below keep their state in. """
# Imports
from stewbeet import Mem, write_load_file

from .definitions import PERK_DEFINITIONS


# Functions
def write_perk_effect_state() -> None:
	ns: str = Mem.ctx.project_id

	# Electric Cherry: a reload discharges a shock scaled by how empty the mag was, so dry reloads hit hard.
	# Anti-spam: the next discharge needs a full 10s cooldown, or 5s plus a dry reload.
	# The last-shock time is a gametime stamp, monotonic and surviving /reload.
	write_load_file(f"""
# Electric Cherry: last-discharge gametime stamp (anti-spam cooldown)
scoreboard objectives add {ns}.zb.ec_last dummy
# Widow's Wine: last web-on-hurt burst gametime stamp (passive cooldown)
scoreboard objectives add {ns}.zb.ww_last dummy
# Dying Wish: use count (escalates cooldown), cooldown countdown, and active berserk timer
scoreboard objectives add {ns}.zb.dw_uses dummy
scoreboard objectives add {ns}.zb.dw_cd dummy
scoreboard objectives add {ns}.zb.dw_timer dummy
# Tombstone: marker state (0 pending / 1 active) + recovery countdown; the marker also carries the
# owner's zb.downed_id so the existing downed_id_match predicate can select it.
scoreboard objectives add {ns}.zb.ts.state dummy
scoreboard objectives add {ns}.zb.ts.timer dummy
# Tombstone: per-perk snapshot of what the owner had when they went down (restored on recovery)
{chr(10).join(f"scoreboard objectives add {ns}.zb.tsp.{pid} dummy" for pid in PERK_DEFINITIONS)}
""")

