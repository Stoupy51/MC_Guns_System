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
	def spawn_category_lines(mode: str, storage_key: str, spawn_tag: str) -> str:
		""" Return the lines feeding one spawn category of a map into ``<mode>/summon_spawn_iter``.

		Args:
			mode        (str): Path segment, e.g. "multiplayer" | "zombies" | "missions".
			storage_key (str): The key under ``game.map.spawning_points`` holding this category.
			spawn_tag   (str): Tag suffix every marker of this category is summoned with.
		Returns:
			str: Three commands, one per line.

		Examples:
			>>> CoreSpawning.spawn_category_lines("zombies", "players", "spawn_zb_player").count("\\n")
			2
		"""
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version
		return f"""data modify storage {ns}:temp _spawn_iter set from storage {ns}:{mode} game.map.spawning_points.{storage_key}
data modify storage {ns}:temp _spawn_tag set value "{ns}.{spawn_tag}"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/{mode}/summon_spawn_iter"""

	@staticmethod
	def write_array_spawn_iter(mode: str) -> None:
		""" Write ``<mode>/summon_spawn_iter`` for the flat ``[x, y, z, yaw]`` map format.

		Zombies has its own iterator instead: its spawns are compounds carrying a group id, an
		activation box and a unique spawn id, none of which exist in this format.
		"""
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version
		write_versioned_function(f"{mode}/summon_spawn_iter", f"""
# Read relative coords
execute store result score #sx {ns}.data run data get storage {ns}:temp _spawn_iter[0][0]
execute store result score #sy {ns}.data run data get storage {ns}:temp _spawn_iter[0][1]
execute store result score #sz {ns}.data run data get storage {ns}:temp _spawn_iter[0][2]
execute store result score #syaw {ns}.data run data get storage {ns}:temp _spawn_iter[0][3] 100

# Convert to absolute
scoreboard players operation #sx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #sy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #sz {ns}.data += #gm_base_z {ns}.data

# Store position + yaw for macro
execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #sx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #sy {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #sz {ns}.data
execute store result storage {ns}:temp _spos.yaw double 0.01 run scoreboard players get #syaw {ns}.data
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_tag

# Summon
function {ns}:v{version}/{mode}/summon_spawn_at with storage {ns}:temp _spos

# Next
data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/{mode}/summon_spawn_iter
""")

	@staticmethod
	def write_random_spawn_selection(mode: str, spawn_tag: str, in_game_score: str, required_tags: tuple[str, ...] = ()) -> None:
		""" Write ``<mode>/{tp_all_to_spawns,pick_spawn,respawn_tp}`` — the "any free marker" flavour.

		Multiplayer does not use this: it scores every candidate by distance to the nearest enemy and
		needs a per-team spawn type, so its three functions stay its own.

		Args:
			mode          (str):   Path segment, "zombies" or "missions".
			spawn_tag     (str):   Tag suffix marking a spawn this mode may send a player to.
			in_game_score (str):   Objective suffix that is 1 while a player is in this mode's game.
			required_tags (tuple): Further tag suffixes a marker must carry; zombies passes ``("spawn_unlocked",)``.
		"""
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version
		candidates: str = f"tag={ns}.spawn_point,tag={ns}.{spawn_tag}" + "".join(f",tag={ns}.{tag}" for tag in required_tags)

		write_versioned_function(f"{mode}/tp_all_to_spawns", f"""
# Teleport every player in this game onto a spawn marker, then free the markers again
execute as @a[scores={{{ns}.{in_game_score}=1}}] at @s run function {ns}:v{version}/{mode}/pick_spawn
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

		write_versioned_function(f"{mode}/pick_spawn", f"""
tag @s add {ns}.spawn_pending

# Tag candidate spawns (exclude used). Capture via command success whether any marker was tagged,
# so the "all used" fallback can branch on a score instead of a global @e existence scan.
execute store success score #has_candidate {ns}.data run tag @e[{candidates},tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# If all used, re-tag them all
execute if score #has_candidate {ns}.data matches 0 run tag @e[{candidates}] add {ns}.spawn_candidate

# Pick random candidate
execute as @n[tag={ns}.spawn_candidate,sort=random] run function {ns}:v{version}/shared/tp_to_spawn {{mode:"{mode}"}}

# Cleanup
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
""")

		write_versioned_function(f"{mode}/respawn_tp", f"""
execute if entity @e[tag={ns}.spawn_point,tag={ns}.{spawn_tag}] run function {ns}:v{version}/{mode}/pick_spawn
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

