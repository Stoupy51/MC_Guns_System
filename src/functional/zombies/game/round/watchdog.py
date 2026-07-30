""" The watchdog that rebuilds a frozen round, and the manual recovery hatch behind it.

Horde ambience used to live here; it moved to enemies/vocals.py when it grew the rest of the Black Ops 2
vocal channels (attack, sprint, death), which are one feature rather than an ambience footnote.
"""
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_function, write_versioned_function

from ....helpers import MGS_TAG


# Functions
def write_watchdog() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Freeze watchdog.
	# A round advances through one handoff chain: spawn -> die -> round_complete -> (5s) -> start_round.
	# Any link can go missing (function that failed to load, schedule dropped on /reload, desynced counter, spawn pass that tagged nothing) and the match then sits at "0 zombies" forever.
	# Rather than enumerating those, watch the property they all share: nothing alive, nothing queued, nothing changing — impossible during real play, where the longest legitimate pause is the 5s handoff.
	write_versioned_function("zombies/watchdog_tick", f"""
# Progress fingerprint: any spawn, kill, or portal strike moves it.
scoreboard players operation #zb_wd_fp {ns}.data = #zb_alive {ns}.data
scoreboard players operation #zb_wd_fp {ns}.data += #zb_to_spawn {ns}.data
scoreboard players operation #zb_wd_fp {ns}.data += #zb_dog_pending {ns}.data

# Anything alive counts as progress on its own: kiting a horde is a normal, arbitrarily long state,
# and unreachable zombies are already handled by the stuck escort/glow system.
scoreboard players set #zb_wd_moved {ns}.data 0
execute if score #zb_alive {ns}.data matches 1.. run scoreboard players set #zb_wd_moved {ns}.data 1
execute unless score #zb_wd_fp {ns}.data = #zb_wd_last {ns}.data run scoreboard players set #zb_wd_moved {ns}.data 1
scoreboard players operation #zb_wd_last {ns}.data = #zb_wd_fp {ns}.data

execute if score #zb_wd_moved {ns}.data matches 1 run scoreboard players set #zb_wd_ticks {ns}.data 0
execute if score #zb_wd_moved {ns}.data matches 0 run scoreboard players add #zb_wd_ticks {ns}.data 1

# 400 ticks = 20s, well past the 5s handoff so a healthy round can't trip it.
execute if score #zb_wd_ticks {ns}.data matches 400.. run function {ns}:zombies/recover
""")

	## Rebuild a frozen round.
	## Also the manual escape hatch (admin button / typed in chat), so a stuck game never needs a restart — version-less so it stays typeable without the pack version.
	write_function(f"{ns}:zombies/recover", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]

scoreboard players set #zb_wd_ticks {ns}.data 0

# Blockers that hold a round open without showing in the sidebar: a desynced dog-portal counter,
# and portals that never struck (their dogs are lost either way).
scoreboard players set #zb_dog_pending {ns}.data 0
kill @e[tag={ns}.dog_portal]

# Drop any handoff still in flight so recovery can't race a schedule landing a tick later
schedule clear {ns}:v{version}/zombies/start_round

tellraw @a [{MGS_TAG},{{"text":"Round was frozen — recovering.","color":"yellow"}}]

# Case A: round_complete ran (it parks #zb_to_spawn at -1) but start_round never landed
execute if score #zb_to_spawn {ns}.data matches ..-1 run return run function {ns}:v{version}/zombies/start_round

# Case B: map empty and nothing queued, but the round never closed — close it
kill @e[tag={ns}.zombie_round]
scoreboard players set #zb_to_spawn {ns}.data 0
function {ns}:v{version}/zombies/round_complete
""")

