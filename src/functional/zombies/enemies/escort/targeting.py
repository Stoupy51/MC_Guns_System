""" Where a trader walks: the monkey lure, the PaP-room lure, or the nearest live player. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers.probes import Probe
from .shared import PATHFINDING_RANGE, PATHFINDING_TIERS, RETARGET_MOVE


# Functions
def write_escort_targeting() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Escorted zombies are glued to their trader, so the nearest trader is theirs.
	my_trader: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,distance=..8]"
	nearest_alive: str = f"@p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]"
	near: str = f"{1 - RETARGET_MOVE}..{RETARGET_MOVE - 1}"

	# Every second: the goal clears wander_target whenever it deactivates.
	write_versioned_function("zombies/escort/retarget", f"""
# The monkey flag outranks the PaP lure and player targeting.
execute if entity @s[tag={ns}.zb_escort_monkey] run return run function {ns}:v{version}/zombies/escort/retarget_monkey

# Walk-to: the trader carries the fixed destination (WanderToPositionGoal.stop() nulls wander_target).
execute if entity @s[tag={ns}.zb_escort_walk] run return run function {ns}:v{version}/zombies/escort/set_wander_target with entity @s data.walk_to

execute if score #zb_lure {ns}.data matches 1 if entity @e[tag={ns}.lure_center] run return run function {ns}:v{version}/zombies/escort/retarget_lure
{Probe.pos(nearest_alive)}
execute store result storage {ns}:temp _escort.x int 1 run data get storage {ns}:temp _probe_pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get storage {ns}:temp _probe_pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get storage {ns}:temp _probe_pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	# Run as the trader, at it.
	write_versioned_function("zombies/escort/retarget_lure", f"""
execute store result storage {ns}:temp _escort.x int 1 run data get entity @n[tag={ns}.lure_center] Pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get entity @n[tag={ns}.lure_center] Pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get entity @n[tag={ns}.lure_center] Pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	# A detonation mid-call keeps the old heading.
	write_versioned_function("zombies/escort/retarget_monkey", f"""
execute store result storage {ns}:temp _escort.x int 1 run data get entity @n[tag={ns}.monkey_bomb] Pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get entity @n[tag={ns}.monkey_bomb] Pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get entity @n[tag={ns}.monkey_bomb] Pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	# Run as the escorted zombie; idempotent and reverts on its own.
	write_versioned_function("zombies/escort/redirect_to_monkey", f"""
tag {my_trader} add {ns}.zb_escort_monkey
""")

	# Run as the trader. The tier follows the trader's progress, so it is picked even when wander_target is kept.
	write_versioned_function("zombies/escort/set_wander_target", f"""
$execute positioned $(x) $(y) $(z) run function {ns}:v{version}/zombies/escort/pick_range

$scoreboard players set #zb_esc_dx {ns}.data $(x)
$scoreboard players set #zb_esc_dy {ns}.data $(y)
$scoreboard players set #zb_esc_dz {ns}.data $(z)
scoreboard players operation #zb_esc_dx {ns}.data -= @s {ns}.zb.escort_tx
scoreboard players operation #zb_esc_dy {ns}.data -= @s {ns}.zb.escort_ty
scoreboard players operation #zb_esc_dz {ns}.data -= @s {ns}.zb.escort_tz
execute if score #zb_esc_dx {ns}.data matches {near} if score #zb_esc_dy {ns}.data matches {near} if score #zb_esc_dz {ns}.data matches {near} if data entity @s wander_target run return 0

$data modify entity @s wander_target set value [I;$(x),$(y),$(z)]
$scoreboard players set @s {ns}.zb.escort_tx $(x)
$scoreboard players set @s {ns}.zb.escort_ty $(y)
$scoreboard players set @s {ns}.zb.escort_tz $(z)
""")

	# Run as the trader, at its target. Rewriting follow_range recomputes the A* budget, hence only on a tier change.
	tiers: str = "\n".join(
		f"execute if entity @s[distance=..{cap}] run return run function {ns}:v{version}/zombies/escort/set_range {{range:{follow_range}}}"
		for cap, follow_range in PATHFINDING_TIERS.items()
	)
	write_versioned_function("zombies/escort/pick_range", f"""
{tiers}
function {ns}:v{version}/zombies/escort/set_range {{range:{PATHFINDING_RANGE}}}
""")

	write_versioned_function("zombies/escort/set_range", f"""
$execute if score @s {ns}.zb.escort_range matches $(range) run return 0
$scoreboard players set @s {ns}.zb.escort_range $(range)
$attribute @s minecraft:follow_range base set $(range)
""")

