""" Spawn markers and picking one to respawn at. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...core.spawning import CoreSpawning


# Functions
def write_missions_spawns() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Spawn Point Markers.
	write_versioned_function("missions/summon_spawns", f"""
# Mission spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:missions game.map.spawning_points.mission
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_mission"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/missions/summon_spawn_iter
""")

	write_versioned_function("missions/summon_spawn_iter", f"""
execute store result score #sx {ns}.data run data get storage {ns}:temp _spawn_iter[0][0]
execute store result score #sy {ns}.data run data get storage {ns}:temp _spawn_iter[0][1]
execute store result score #sz {ns}.data run data get storage {ns}:temp _spawn_iter[0][2]
execute store result score #syaw {ns}.data run data get storage {ns}:temp _spawn_iter[0][3] 100

scoreboard players operation #sx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #sy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #sz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #sx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #sy {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #sz {ns}.data
execute store result storage {ns}:temp _spos.yaw double 0.01 run scoreboard players get #syaw {ns}.data
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_tag

function {ns}:v{version}/missions/summon_spawn_at with storage {ns}:temp _spos

data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/missions/summon_spawn_iter
""")

	CoreSpawning.write_summon_spawn_at("missions")

	# Smart Spawn Teleportation.
	write_versioned_function("missions/tp_all_to_spawns", f"""
# Teleport all players to mission spawns (random selection)
execute as @a[scores={{{ns}.mi.in_game=1}}] at @s run function {ns}:v{version}/missions/pick_spawn
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

	write_versioned_function("missions/pick_spawn", f"""
tag @s add {ns}.spawn_pending

# Tag candidate spawns (exclude used). Capture via command success whether any marker was tagged,
# so the "all used" fallback can branch on a score instead of a global @e existence scan.
execute store success score #has_candidate {ns}.data run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_mission,tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# If all used, re-tag all
execute if score #has_candidate {ns}.data matches 0 run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_mission] add {ns}.spawn_candidate

# Pick random candidate
execute as @n[tag={ns}.spawn_candidate,sort=random] run function {ns}:v{version}/shared/tp_to_spawn {{mode:"missions"}}

# Cleanup
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
""")

	## Respawn TP for missions (run as the respawning player)
	write_versioned_function("missions/respawn_tp", f"""
execute if entity @e[tag={ns}.spawn_point,tag={ns}.spawn_mission] run function {ns}:v{version}/missions/pick_spawn
""")

