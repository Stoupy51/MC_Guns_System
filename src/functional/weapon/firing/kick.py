""" Weapon recoil: rotates the player's view by the weapon's kick value. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import KICK


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("player/right_click", f"""
function {ns}:v{version}/kicks/main
""")

	write_versioned_function("kicks/main", f"""
# Kick type, and a random value from 1 to 5.
scoreboard players set #kick {ns}.data 0
execute store result score #kick {ns}.data run data get storage {ns}:gun all.stats.{KICK}
execute store result score #random {ns}.data run random value 1..5

# In a vehicle, /rotate instead of /tp, which would dismount.
scoreboard players set #has_vehicle {ns}.data 0
execute on vehicle run scoreboard players set #has_vehicle {ns}.data 1

# Deadshot Daiquiri (zombies): the 65% kick tables.
execute if score @s {ns}.special.deadshot matches 1 run return run function {ns}:v{version}/kicks/apply_ds

function {ns}:v{version}/kicks/apply
""")

	# Shared by the normal and Deadshot (_ds) kick tables.
	kick_ranges: list[str] = ["..0", "1", "2", "3", "4", "5.."]

	def kick_switch(suffix: str) -> str:
		return "\n".join(
			f"execute if score #kick {ns}.data matches {rng} run function {ns}:v{version}/kicks/type_{i}{suffix}"
			for i, rng in enumerate(kick_ranges)
		)
	write_versioned_function("kicks/apply", kick_switch(""))
	write_versioned_function("kicks/apply_ds", kick_switch("_ds"))

	all_kicks: list[list[tuple[float, float]]] = [
		[(-0.05, -0.25), (-0.025, -0.25), (-0.0, -0.25), (0.025, -0.25), (0.05, -0.25)],
		[(-0.08, -0.5), (-0.03, -0.5), (-0.0, -0.5), (0.03, -0.5), (0.08, -0.5)],
		[(-0.11, -1.0), (-0.05, -1.0), (-0.0, -1.0), (0.05, -1.0), (0.11, -1.0)],
		[(-0.13, -1.5), (-0.06, -1.5), (-0.0, -1.5), (0.06, -1.5), (0.13, -1.5)],
		[(-0.15, -2.0), (-0.06, -2.0), (-0.0, -2.0), (0.06, -2.0), (0.15, -2.0)],
		[(-0.17, -2.5), (-0.06, -2.5), (-0.0, -2.5), (0.06, -2.5), (0.17, -2.5)],
	]
	# Deadshot Daiquiri: -35% recoil, the same tables at 65%.
	for suffix, factor in [("", 1.0), ("_ds", 0.65)]:
		for i, kicks in enumerate(all_kicks):
			content: str = ""
			for score, command in [(0, "tp @s ~ ~ ~"), (1, "rotate @s")]:
				for j, (yaw, pitch) in enumerate(kicks):
					sy: float = round(yaw * factor, 4)
					sp: float = round(pitch * factor, 4)
					content += f"\nexecute if score #has_vehicle {ns}.data matches {score} if score #random {ns}.data matches {j+1} run {command} ~{sy} ~{sp}"
			write_versioned_function(f"kicks/type_{i}{suffix}", content)

