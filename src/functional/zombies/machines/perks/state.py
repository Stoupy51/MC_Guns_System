""" Scores and storage the active perk effects below keep their state in. """
# Imports
from stewbeet import Mem, write_load_file

from .definitions import TOMBSTONE_PERKS


# Functions
def write_perk_effect_state() -> None:
	ns: str = Mem.ctx.project_id

	# Electric Cherry: a reload discharges a shock scaled by how empty the magazine was. The next one needs 10 s,
	# or 5 s and a dry reload; the stamp is gametime, which survives /reload.
	write_load_file(f"""
# Last discharge (gametime).
scoreboard objectives add {ns}.zb.ec_last dummy
# Widow's Wine: last web burst (gametime).
scoreboard objectives add {ns}.zb.ww_last dummy
# Dying Wish: uses (escalating cooldown), cooldown, berserk timer.
scoreboard objectives add {ns}.zb.dw_uses dummy
scoreboard objectives add {ns}.zb.dw_cd dummy
scoreboard objectives add {ns}.zb.dw_timer dummy
# Tombstone: state (0 pending, 1 active) and recovery timer; the marker also carries zb.downed_id for downed_id_match.
scoreboard objectives add {ns}.zb.ts.state dummy
scoreboard objectives add {ns}.zb.ts.timer dummy
# Tombstone: the owner's perks when they went down.
{chr(10).join(f"scoreboard objectives add {ns}.zb.tsp.{pid} dummy" for pid in TOMBSTONE_PERKS)}
""")

