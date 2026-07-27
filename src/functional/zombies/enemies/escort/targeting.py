""" Where a trader walks: the monkey lure, the PaP-room lure, or the nearest live player. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_escort_targeting() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Escorted zombies are glued to their trader every tick, so "mine" is always the nearest one
	my_trader: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,distance=..8]"
	nearest_alive: str = f"@p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]"

	# Refresh wander_target every second (the goal clears it whenever it deactivates)
	write_versioned_function("zombies/escort/retarget", f"""
# Monkey-bomb lure (monkey_bomb.py): aim at the nearest thrown monkey — takes priority over both
# the PaP lure and player targeting while the trader carries the {ns}.zb_escort_monkey flag.
execute if entity @s[tag={ns}.zb_escort_monkey] run return run function {ns}:v{version}/zombies/escort/retarget_monkey

# PaP-room lure active: aim at the theatre centre marker instead of a player (see escort.py)
execute if score #zb_lure {ns}.data matches 1 if entity @e[tag={ns}.lure_center] run return run function {ns}:v{version}/zombies/escort/retarget_lure
execute store result storage {ns}:temp _escort.x int 1 run data get entity {nearest_alive} Pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get entity {nearest_alive} Pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get entity {nearest_alive} Pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	# Aim the trader at the theatre centre marker (@s = trader, at @s)
	write_versioned_function("zombies/escort/retarget_lure", f"""
execute store result storage {ns}:temp _escort.x int 1 run data get entity @n[tag={ns}.lure_center] Pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get entity @n[tag={ns}.lure_center] Pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get entity @n[tag={ns}.lure_center] Pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	# Aim the trader at the nearest thrown monkey; a detonation mid-call just keeps the old heading
	write_versioned_function("zombies/escort/retarget_monkey", f"""
execute store result storage {ns}:temp _escort.x int 1 run data get entity @n[tag={ns}.monkey_bomb] Pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get entity @n[tag={ns}.monkey_bomb] Pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get entity @n[tag={ns}.monkey_bomb] Pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	# Redirect a running escort to a monkey (@s = escorted zombie); idempotent, reverts on its own
	write_versioned_function("zombies/escort/redirect_to_monkey", f"""
tag {my_trader} add {ns}.zb_escort_monkey
""")

	write_versioned_function("zombies/escort/set_wander_target", """
$data modify entity @s wander_target set value [I;$(x),$(y),$(z)]
""")

