""" The game tick and preload hooks. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_pap_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Hook PAP animation into the game tick loop.
	write_versioned_function("zombies/game_tick", f"""
# PAP animation tick (all phases use positive timer: 300→0)
execute as @e[type=minecraft:interaction,tag={ns}.pap_machine,scores={{{ns}.pap_anim=1..}}] at @s run function {ns}:v{version}/zombies/pap/anim/step

# Timeslip: two extra steps this tick for Timeslip-owned machines (3x total speed)
execute as @e[type=minecraft:interaction,tag={ns}.pap_machine,scores={{{ns}.zb.pap.timeslip=1,{ns}.pap_anim=1..}}] at @s run function {ns}:v{version}/zombies/pap/anim/step_timeslip
""")

	# Hook into preload_complete to spawn PAP machine interactions.
	write_versioned_function("zombies/preload_complete", f"""
# Setup Pack-a-Punch machines
execute if data storage {ns}:zombies game.map.pap_machines[0] run function {ns}:v{version}/zombies/pap/setup
""")

