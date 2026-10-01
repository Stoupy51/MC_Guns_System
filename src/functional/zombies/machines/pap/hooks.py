""" The game tick and preload hooks. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_pap_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/game_tick", f"""
# The timer counts down from 300.
execute as @e[type=minecraft:interaction,tag={ns}.pap_machine,scores={{{ns}.pap_anim=1..}}] at @s run function {ns}:v{version}/zombies/pap/anim/step

# Timeslip: two extra steps per tick (3x).
execute as @e[type=minecraft:interaction,tag={ns}.pap_machine,scores={{{ns}.zb.pap.timeslip=1,{ns}.pap_anim=1..}}] at @s run function {ns}:v{version}/zombies/pap/anim/step_timeslip
""")

	write_versioned_function("zombies/preload_complete", f"""
execute if data storage {ns}:zombies game.map.pap_machines[0] run function {ns}:v{version}/zombies/pap/setup
""")

