""" Shared OOB + spawn marker summoning functions. """
# Imports
from stewbeet import Mem, write_versioned_function


# Classes
class CoreSpawning:
	""" Spawning helpers. """

	# Functions
	@staticmethod
	def write_spawn_teleport() -> None:
		""" Write the two teleport functions, shared because their bodies name no mode of their own.

		`shared/tp_to_spawn` runs as the chosen marker and moves whoever is tagged `spawn_pending` onto
		it. Its `mode` argument only names the storage holding that mode's game state: a marker is
		consumed once during the pre-game teleport, but a respawn mid-game must be able to reuse it.
		"""
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		write_versioned_function("shared/tp_player_at", "$tp @s $(x) $(y) $(z) $(yaw) 0")

		write_versioned_function("shared/tp_to_spawn", f"""
# Store marker position and yaw for the teleport macro
execute store result storage {ns}:temp _tp.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _tp.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _tp.z double 1 run data get entity @s Pos[2]
data modify storage {ns}:temp _tp.yaw set from entity @s data.yaw

# TP the pending player
execute as @p[tag={ns}.spawn_pending] run function {ns}:v{version}/shared/tp_player_at with storage {ns}:temp _tp

# Mark this spawn as used (prevents duplicate assignments) (only in preparing time)
$execute unless data storage {ns}:$(mode) game{{state:"active"}} run tag @s add {ns}.spawn_used
""")

	@staticmethod
	def write_summon_spawn_at(mode: str, extra_spawn_tags: tuple[str, ...] = ()) -> None:
		""" Write ``<mode>/summon_spawn_at`` — the macro summoning a spawn-point marker.

		Args:
			mode             (str):   Path segment, e.g. "multiplayer" | "zombies" | "missions".
			extra_spawn_tags (tuple): Extra tag suffixes (without the ``<ns>.`` prefix); zombies passes ``("new_spawn",)``.
		"""
		ns: str = Mem.ctx.project_id
		tags: str = f'"{ns}.spawn_point","$(tag)","{ns}.gm_entity"'
		for tag in extra_spawn_tags:
			tags += f',"{ns}.{tag}"'
		write_versioned_function(f"{mode}/summon_spawn_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:[{tags}],data:{{yaw:$(yaw)}}}}
""")

	@staticmethod
	def write_shared_spawning_functions() -> None:
			ns: str = Mem.ctx.project_id
			version: str = Mem.ctx.project_version

			## Summon OOB markers from map data (relative → absolute) Usage: function shared/summon_oob {mode:"multiplayer"}
			write_versioned_function("shared/summon_oob", f"""
$function {ns}:v{version}/shared/load_base_coordinates {{mode:"$(mode)"}}

$data modify storage {ns}:temp _oob_iter set from storage {ns}:$(mode) game.map.out_of_bounds
execute if data storage {ns}:temp _oob_iter[0] run function {ns}:v{version}/shared/summon_oob_iter
""")

			write_versioned_function("shared/summon_oob_iter", f"""
execute store result score #rx {ns}.data run data get storage {ns}:temp _oob_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _oob_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _oob_iter[0][2]
scoreboard players operation #rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _oob_pos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _oob_pos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _oob_pos.z double 1 run scoreboard players get #rz {ns}.data
function {ns}:v{version}/shared/summon_oob_at with storage {ns}:temp _oob_pos
data remove storage {ns}:temp _oob_iter[0]
execute if data storage {ns}:temp _oob_iter[0] run function {ns}:v{version}/shared/summon_oob_iter
""")

			write_versioned_function("shared/summon_oob_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.oob_point","{ns}.gm_entity"]}}
""")

