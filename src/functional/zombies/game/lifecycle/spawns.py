""" Spawn markers, their activation boxes and picking one to respawn at. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.spawning import CoreSpawning


# Functions
def write_zombies_spawns() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/summon_spawns", f"""
# Each marker gets the next unique id.
scoreboard players set #zb_spawn_sid {ns}.data 0

{CoreSpawning.spawn_category_lines("zombies", "players", "spawn_zb_player")}

{CoreSpawning.spawn_category_lines("zombies", "zombies", "spawn_zb")}

# Special spawns (dog rounds, later mini-bosses) work like zombie spawns; only the tag differs.
{CoreSpawning.spawn_category_lines("zombies", "special", "spawn_special")}

# From the map data, not an entity scan, so start_round gates dog rounds on a score.
execute store success score #zb_has_special {ns}.data if data storage {ns}:zombies game.map.spawning_points.special[0]

# game_tick and round completion read both flags from the first tick.
scoreboard players set #zb_dog_round {ns}.data 0
scoreboard players set #zb_dog_pending {ns}.data 0

# Group 0 is the starting area.
scoreboard players set #unlock_gid {ns}.data 0
execute as @e[tag={ns}.spawn_point] if score @s {ns}.zb.spawn.gid = #unlock_gid {ns}.data run tag @s add {ns}.spawn_unlocked
""")

	write_versioned_function("zombies/summon_spawn_iter", f"""
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

# Defaults to group 0.
scoreboard players set @n[tag={ns}.new_spawn] {ns}.zb.spawn.gid 0
execute store result score @n[tag={ns}.new_spawn] {ns}.zb.spawn.gid run data get storage {ns}:temp _spawn_iter[0].group_id

# Zombies remember their spawn so they never reuse it.
scoreboard players add #zb_spawn_sid {ns}.data 1
scoreboard players operation @n[tag={ns}.new_spawn] {ns}.zb.spawn.sid = #zb_spawn_sid {ns}.data

# Zombie spawns only: the absolute box [x, y, z, dx, dy, dz] (all 6 needed), so a player standing in it gates the spawn.
execute if data storage {ns}:temp _spawn_iter[0].activation_box[5] run function {ns}:v{version}/zombies/store_spawn_abox

# Zombie spawns only: zombies spawned here are escorted to this absolute spot.
execute if data storage {ns}:temp _spawn_iter[0].walk_to[2] run function {ns}:v{version}/zombies/store_spawn_walk_to

tag @n[tag={ns}.new_spawn] remove {ns}.new_spawn

data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter
""")

	## #sx, #sy, #sz hold the marker position; activation_box[0..2] is the relative corner, [3..5] the size.
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

	## #sx, #sy, #sz hold the marker position, walk_to[0..2] the offset. Three ints, as wander_target and the arrival test expect.
	write_versioned_function("zombies/store_spawn_walk_to", f"""
execute store result score #swx {ns}.data run data get storage {ns}:temp _spawn_iter[0].walk_to[0]
execute store result score #swy {ns}.data run data get storage {ns}:temp _spawn_iter[0].walk_to[1]
execute store result score #swz {ns}.data run data get storage {ns}:temp _spawn_iter[0].walk_to[2]
scoreboard players operation #swx {ns}.data += #sx {ns}.data
scoreboard players operation #swy {ns}.data += #sy {ns}.data
scoreboard players operation #swz {ns}.data += #sz {ns}.data
execute store result storage {ns}:temp _walk_to.x int 1 run scoreboard players get #swx {ns}.data
execute store result storage {ns}:temp _walk_to.y int 1 run scoreboard players get #swy {ns}.data
execute store result storage {ns}:temp _walk_to.z int 1 run scoreboard players get #swz {ns}.data
data modify entity @n[tag={ns}.new_spawn] data.walk_to set from storage {ns}:temp _walk_to
""")

	CoreSpawning.write_summon_spawn_at("zombies", extra_spawn_tags=("new_spawn",))

	CoreSpawning.write_random_spawn_selection("zombies", "spawn_zb_player", "zb.in_game", required_tags=("spawn_unlocked",))

