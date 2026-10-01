""" The watchdog that rebuilds a frozen round, and the manual recovery hatch behind it. """
# Imports
from stewbeet import Mem, write_function, write_versioned_function

from ....helpers import MGS_TAG


# Functions
def write_watchdog() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# A round advances through spawn, die, round_complete, 5 s, start_round, and any link can go missing (failed load, schedule dropped on /reload, desynced counter).
	# The watchdog looks for what they share: nothing alive, nothing queued and nothing changing for longer than the 5 s handoff.
	write_versioned_function("zombies/watchdog_tick", f"""
# Any spawn, kill or portal strike moves it.
scoreboard players operation #zb_wd_fp {ns}.data = #zb_alive {ns}.data
scoreboard players operation #zb_wd_fp {ns}.data += #zb_to_spawn {ns}.data
scoreboard players operation #zb_wd_fp {ns}.data += #zb_dog_pending {ns}.data

# Anything alive is progress: kiting is a normal state, and unreachable zombies are the stuck system's job.
scoreboard players set #zb_wd_moved {ns}.data 0
execute if score #zb_alive {ns}.data matches 1.. run scoreboard players set #zb_wd_moved {ns}.data 1
execute unless score #zb_wd_fp {ns}.data = #zb_wd_last {ns}.data run scoreboard players set #zb_wd_moved {ns}.data 1
scoreboard players operation #zb_wd_last {ns}.data = #zb_wd_fp {ns}.data

execute if score #zb_wd_moved {ns}.data matches 1 run scoreboard players set #zb_wd_ticks {ns}.data 0
execute if score #zb_wd_moved {ns}.data matches 0 run scoreboard players add #zb_wd_ticks {ns}.data 1

# 20 s, well past the 5 s handoff.
execute if score #zb_wd_ticks {ns}.data matches 400.. run function {ns}:zombies/recover
""")

	## Also the manual escape hatch (admin button or chat), unversioned so it stays typeable.
	write_function(f"{ns}:zombies/recover", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]

scoreboard players set #zb_wd_ticks {ns}.data 0

# Hidden blockers: a desynced dog-portal counter, and portals that never struck (their dogs are lost either way).
scoreboard players set #zb_dog_pending {ns}.data 0
kill @e[tag={ns}.dog_portal]

# So recovery cannot race a schedule landing a tick later.
schedule clear {ns}:v{version}/zombies/start_round

tellraw @a [{MGS_TAG},{{"text":"Round was frozen — recovering.","color":"yellow"}}]

# round_complete ran (it parks #zb_to_spawn at -1) but start_round never landed.
execute if score #zb_to_spawn {ns}.data matches ..-1 run return run function {ns}:v{version}/zombies/start_round

# Empty map, nothing queued, round never closed.
kill @e[tag={ns}.zombie_round]
scoreboard players set #zb_to_spawn {ns}.data 0
function {ns}:v{version}/zombies/round_complete
""")

