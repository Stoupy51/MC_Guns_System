""" Ending an escort, whether the zombie arrives, is killed, or the trader is lost. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_escort_end() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Escorted zombies are glued to their trader every tick, so "mine" is always the nearest one
	my_trader: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,distance=..8]"
	my_trader_monkey: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,tag={ns}.zb_escort_monkey,distance=..8]"
	nearest_alive: str = f"@p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]"

	# End the escort and restore the zombie's AI; the trader is the caller's problem
	write_versioned_function("zombies/escort/detach", f"""
tag @s remove {ns}.zb_escorted
data modify entity @s NoAI set value 0b
scoreboard players remove #zb_escort_count {ns}.data 1

# Kickstart vanilla AI. A zombie fresh off NoAI won't re-scan for a target for up to ~0.5s
# (NearestAttackableTargetGoal's mustSee re-scan interval) and looks braindead standing still.
# Turn it to face the nearest player and clear its NoActionTime so the goal selector re-evaluates
# immediately, then a brief speed nudge so it lunges the instant it acquires the target instead
# of pausing. (NoActionTime being high after the frozen transport is what stalls the first scan.)
data modify entity @s NoActionTime set value 0
execute at @s facing entity {nearest_alive} eyes run tp @s ~ ~ ~ ~ ~
effect give @s minecraft:speed 2 0 true

# Fresh stuck-tracking window from wherever the escort left the zombie
scoreboard players set @s {ns}.zb.stuck_dist 4
execute store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
""")

	# Successful delivery: a player is within RELEASE_RADIUS and visible (@s = zombie)
	write_versioned_function("zombies/escort/release", f"""
execute as {my_trader} run function {ns}:v{version}/zombies/escort/discard_trader
function {ns}:v{version}/zombies/escort/detach
""")

	# Remove a trader with zero visible feedback (@s = trader)
	write_versioned_function("zombies/escort/discard_trader", """
tp @s ~ ~-1000 ~
kill @s
""")

	# The trader could not path either; the failure flag routes THIS call to the teleport rescue
	write_versioned_function("zombies/escort/give_up", f"""
# A MONKEY escort must never fall through to the teleport rescue
execute if entity {my_trader_monkey} run return run function {ns}:v{version}/zombies/escort/monkey_hold

tag @s add {ns}.zb_escort_failed
execute as {my_trader} run function {ns}:v{version}/zombies/escort/discard_trader
function {ns}:v{version}/zombies/escort/detach
function {ns}:v{version}/zombies/on_stuck_zombie
""")

	# Escorted zombie killed mid-transit: discard its taxi this tick, not on the 2s sweep
	write_versioned_function("zombies/on_zombie_dying", f"""
# Escorted zombie died: remove its escort trader immediately (escort.py)
execute if entity @s[tag={ns}.zb_escorted] at @s run function {ns}:v{version}/zombies/escort/on_escorted_killed
""", prepend=True)

	# No detach: the zombie is being removed anyway, so just drop the bookkeeping and the trader
	write_versioned_function("zombies/escort/on_escorted_killed", f"""
tag @s remove {ns}.zb_escorted
scoreboard players remove #zb_escort_count {ns}.data 1
execute as {my_trader} run function {ns}:v{version}/zombies/escort/discard_trader
""")

	# End an escort from the TRADER's context; shared by the reach safeguard and barriers.py
	write_versioned_function("zombies/escort/end_at_trader", f"""
execute as @e[tag={ns}.zb_escorted,distance=..8,limit=1,sort=nearest] run function {ns}:v{version}/zombies/escort/detach
function {ns}:v{version}/zombies/escort/discard_trader
""")

