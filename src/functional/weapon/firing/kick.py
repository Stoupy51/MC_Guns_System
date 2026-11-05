""" Weapon recoil: the view climbs over the ticks after a shot, from the weapon's kick level down to level 0. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ....config.stats.keys import KICK


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
scoreboard objectives add {ns}.kick dummy
scoreboard objectives add {ns}.kick_dir dummy
""")

	write_versioned_function("player/right_click", f"""
function {ns}:v{version}/kicks/main
""")
	write_versioned_function("player/tick", f"""
execute if score @s {ns}.kick matches 0.. run function {ns}:v{version}/kicks/tick
""")

	# A shot restarts the climb at the weapon's level, playing that level and every lower one on the following ticks.
	write_versioned_function("kicks/main", f"""
scoreboard players set #kick {ns}.data 0
execute store result score #kick {ns}.data run data get storage {ns}:gun all.stats.{KICK}
execute if score #kick {ns}.data matches ..-1 run scoreboard players set #kick {ns}.data 0
execute if score #kick {ns}.data matches 6.. run scoreboard players set #kick {ns}.data 5
scoreboard players operation @s {ns}.kick = #kick {ns}.data
execute store result score @s {ns}.kick_dir run random value 1..5
""")

	# Deadshot Daiquiri (zombies): the 65% kick tables.
	write_versioned_function("kicks/tick", f"""
execute if score @s {ns}.special.deadshot matches 1 run function {ns}:v{version}/kicks/apply_ds
execute unless score @s {ns}.special.deadshot matches 1 run function {ns}:v{version}/kicks/apply
scoreboard players remove @s {ns}.kick 1
""")

	# Shared by the normal and Deadshot (_ds) kick tables.
	def kick_switch(suffix: str) -> str:
		return "\n".join(
			f"execute if score @s {ns}.kick matches {i} run function {ns}:v{version}/kicks/type_{i}{suffix}"
			for i in range(6)
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
			# /rotate, never /tp: the server drops a player's movement until a teleport is acknowledged, so a gun firing every tick pins them.
			write_versioned_function(f"kicks/type_{i}{suffix}", "\n".join(
				f"execute if score @s {ns}.kick_dir matches {j+1} run rotate @s ~{round(yaw * factor, 4)} ~{round(pitch * factor, 4)}"
				for j, (yaw, pitch) in enumerate(kicks)
			))

