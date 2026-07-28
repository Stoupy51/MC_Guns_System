""" Spawn markers, their activation boxes and picking one to respawn at. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.spawning import CoreSpawning


# Functions
def write_zombies_spawns() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Spawn Point Markers.

	write_versioned_function("zombies/summon_spawns", f"""
# Reset the unique spawn id counter (each summoned marker gets the next id)
scoreboard players set #zb_spawn_sid {ns}.data 0

# Player spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.players
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_zb_player"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter

# Zombie spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.zombies
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_zb"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter

# Special spawns (dog rounds today, mini-bosses later). Same plumbing as zombie spawns — group_id
# gating, activation boxes, unique spawn ids — only the tag differs.
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.special
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_special"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter

# Read off the map data, not an entity scan, so start_round can gate dog rounds on a score
execute store success score #zb_has_special {ns}.data if data storage {ns}:zombies game.map.spawning_points.special[0]

# Both flags must exist before the first tick: game_tick and round completion gate on them
scoreboard players set #zb_dog_round {ns}.data 0
scoreboard players set #zb_dog_pending {ns}.data 0

# Tag group 0 spawns as unlocked (starting area)
scoreboard players set #unlock_gid {ns}.data 0
execute as @e[tag={ns}.spawn_point] if score @s {ns}.zb.spawn.gid = #unlock_gid {ns}.data run tag @s add {ns}.spawn_unlocked
""")

	write_versioned_function("zombies/summon_spawn_iter", f"""
# Read position from compound format
execute store result score #sx {ns}.data run data get storage {ns}:temp _spawn_iter[0].pos[0]
execute store result score #sy {ns}.data run data get storage {ns}:temp _spawn_iter[0].pos[1]
execute store result score #sz {ns}.data run data get storage {ns}:temp _spawn_iter[0].pos[2]
execute store result score #syaw {ns}.data run data get storage {ns}:temp _spawn_iter[0].rotation[0] 100

scoreboard players operation #sx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #sy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #sz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #sx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #sy {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #sz {ns}.data
execute store result storage {ns}:temp _spos.yaw double 0.01 run scoreboard players get #syaw {ns}.data
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_tag

function {ns}:v{version}/zombies/summon_spawn_at with storage {ns}:temp _spos

# Set group_id score on newly spawned marker (default 0 if not defined)
scoreboard players set @n[tag={ns}.new_spawn] {ns}.zb.spawn.gid 0
execute store result score @n[tag={ns}.new_spawn] {ns}.zb.spawn.gid run data get storage {ns}:temp _spawn_iter[0].group_id

# Assign a unique spawn id (lets zombies remember their previous spawn point and never reuse it)
scoreboard players add #zb_spawn_sid {ns}.data 1
scoreboard players operation @n[tag={ns}.new_spawn] {ns}.zb.spawn.sid = #zb_spawn_sid {ns}.data

# Optional activation box (zombie spawns only): store the ABSOLUTE box on the marker so the
# round spawner can gate this spawn on a player standing inside it. Only present when the map
# data defines all 6 elements [x,y,z,dx,dy,dz] (relative to this spawn).
execute if data storage {ns}:temp _spawn_iter[0].activation_box[5] run function {ns}:v{version}/zombies/store_spawn_abox

tag @n[tag={ns}.new_spawn] remove {ns}.new_spawn

data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter
""")

	## Store the absolute activation box {x,y,z,dx,dy,dz} on the just-summoned spawn marker.
	# #sx/#sy/#sz hold the marker's absolute coords.
	# activation_box[0..2] are the relative corner offset and [3..5] the box size, in blocks.
	write_versioned_function("zombies/store_spawn_abox", f"""
execute store result score #abx {ns}.data run data get storage {ns}:temp _spawn_iter[0].activation_box[0]
execute store result score #aby {ns}.data run data get storage {ns}:temp _spawn_iter[0].activation_box[1]
execute store result score #abz {ns}.data run data get storage {ns}:temp _spawn_iter[0].activation_box[2]
scoreboard players operation #abx {ns}.data += #sx {ns}.data
scoreboard players operation #aby {ns}.data += #sy {ns}.data
scoreboard players operation #abz {ns}.data += #sz {ns}.data
execute store result storage {ns}:temp _abox.x double 1 run scoreboard players get #abx {ns}.data
execute store result storage {ns}:temp _abox.y double 1 run scoreboard players get #aby {ns}.data
execute store result storage {ns}:temp _abox.z double 1 run scoreboard players get #abz {ns}.data
execute store result storage {ns}:temp _abox.dx double 1 run data get storage {ns}:temp _spawn_iter[0].activation_box[3]
execute store result storage {ns}:temp _abox.dy double 1 run data get storage {ns}:temp _spawn_iter[0].activation_box[4]
execute store result storage {ns}:temp _abox.dz double 1 run data get storage {ns}:temp _spawn_iter[0].activation_box[5]
data modify entity @n[tag={ns}.new_spawn] data.abox set from storage {ns}:temp _abox
""")

	CoreSpawning.write_summon_spawn_at("zombies", extra_spawn_tags=("new_spawn",))

	# Smart Spawn Selection.

	write_versioned_function("zombies/tp_all_to_spawns", f"""
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/pick_spawn
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

	write_versioned_function("zombies/pick_spawn", f"""
tag @s add {ns}.spawn_pending

# Tag candidate spawns (unlocked, exclude used). Capture via command success whether any marker
# was tagged, so the "all used" fallback can branch on a score instead of a global @e scan.
execute store success score #has_candidate {ns}.data run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked,tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# If all used, re-tag all unlocked
execute if score #has_candidate {ns}.data matches 0 run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate

# Pick random candidate
execute as @n[tag={ns}.spawn_candidate,sort=random] run function {ns}:v{version}/shared/tp_to_spawn {{mode:"zombies"}}

# Cleanup
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
""")

	## Respawn TP for zombies
	write_versioned_function("zombies/respawn_tp", f"""
execute if entity @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player] run function {ns}:v{version}/zombies/pick_spawn
""")

