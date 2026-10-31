""" Spawn markers: their kinds and defaults, and the tags saying which of them can be used right now. """
# Imports
from dataclasses import dataclass, field
from typing import Any

from stewbeet import JsonDict, Mem, write_load_file, write_versioned_function

from ....core.spawning import CoreSpawning
from ....helpers.snbt import snbt


# Classes
@dataclass(frozen=True)
class SpawnKind:
	""" One category of a zombies map's spawn markers, under game.map.spawning_points. """
	key: str
	tag: str
	""" Tag suffix of its markers. """
	name: str
	""" In-game name of its markers, followed by their id and group. """
	defaults: JsonDict = field(default_factory=dict[str, Any])
	""" What an entry without one of these fields behaves as, and what the editor places new ones with. """


# Constants
ENEMY_SPAWN_DEFAULTS: JsonDict = {"activation_box": [], "walk_to": [], "rise_ticks": 20, "min_round": 0, "max_round": 0}
PLAYER_SPAWNS: SpawnKind = SpawnKind(key="players", tag="spawn_zb_player", name="Player Spawn")
ZOMBIE_SPAWNS: SpawnKind = SpawnKind(key="zombies", tag="spawn_zb", name="Zombie Spawn", defaults={
	**ENEMY_SPAWN_DEFAULTS, "arrival": "floor", "power": False, "mob": {"entity": "zombie"},
})
SPECIAL_SPAWNS: SpawnKind = SpawnKind(key="special", tag="spawn_special", name="Special Spawn", defaults={
	**ENEMY_SPAWN_DEFAULTS, "arrival": "portal", "mob": {"entity": "wolf"},
})
""" Special rounds draw from these only, normal rounds from zombie spawns only. """
ENEMY_SPAWNS: tuple[SpawnKind, ...] = (ZOMBIE_SPAWNS, SPECIAL_SPAWNS)

ARRIVALS: tuple[str, ...] = ("floor", "ceiling", "portal", "instant")
""" How a spawn's enemy comes in, each tagged `arrive_<arrival>` on its marker. """


# Functions
def open_spawn(ns: str) -> str:
	""" Selector arguments of a spawn usable right now: door opened, round in its bounds, power on if it needs it, a player in its box if it has one.

	>>> open_spawn("mgs")
	'type=minecraft:marker,tag=mgs.spawn_unlocked,tag=mgs.spawn_round_ok,tag=mgs.spawn_powered,tag=mgs.spawn_abox_ok'
	"""
	return f"type=minecraft:marker,tag={ns}.spawn_unlocked,tag={ns}.spawn_round_ok,tag={ns}.spawn_powered,tag={ns}.spawn_abox_ok"


def write_zombies_spawns() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
# A spawn's round bounds, min_round and max_round (no limit stored as the int maximum).
scoreboard objectives add {ns}.zb.spawn.rmin dummy
scoreboard objectives add {ns}.zb.spawn.rmax dummy
""")

	categories: str = "\n\n".join(
		f"data modify storage {ns}:temp _spawn_defaults set value {snbt(kind.defaults)}\n"
		+ CoreSpawning.spawn_category_lines("zombies", kind.key, kind.tag, kind.name)
		for kind in (PLAYER_SPAWNS, *ENEMY_SPAWNS)
	)
	write_versioned_function("zombies/summon_spawns", f"""
# Each marker gets the next unique id.
scoreboard players set #zb_spawn_sid {ns}.data 0

{categories}

# game_tick and round completion read both from the first tick.
scoreboard players set #zb_special_round {ns}.data 0
scoreboard players set #zb_portal_pending {ns}.data 0

# Group 0 is the starting area.
scoreboard players set #unlock_gid {ns}.data 0
execute as @e[type=minecraft:marker,tag={ns}.spawn_point] if score @s {ns}.zb.spawn.gid = #unlock_gid {ns}.data run tag @s add {ns}.spawn_unlocked
""")

	write_versioned_function("zombies/summon_spawn_iter", f"""
# The kind's defaults stand in for the fields the map leaves out.
data modify storage {ns}:temp _spawn set from storage {ns}:temp _spawn_defaults
data modify storage {ns}:temp _spawn merge from storage {ns}:temp _spawn_iter[0]

execute store result score #sx {ns}.data run data get storage {ns}:temp _spawn.pos[0]
execute store result score #sy {ns}.data run data get storage {ns}:temp _spawn.pos[1]
execute store result score #sz {ns}.data run data get storage {ns}:temp _spawn.pos[2]
execute store result score #syaw {ns}.data run data get storage {ns}:temp _spawn.rotation[0] 100

scoreboard players operation #sx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #sy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #sz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #sx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #sy {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #sz {ns}.data
execute store result storage {ns}:temp _spos.yaw double 0.01 run scoreboard players get #syaw {ns}.data
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_tag

# "Zombie Spawn #12 (group 2)": zombies remember their spawn's id so the stuck rescue never reuses it.
scoreboard players add #zb_spawn_sid {ns}.data 1
data modify storage {ns}:temp _spawn_label set value {{group_id:0}}
data modify storage {ns}:temp _spawn_label.name set from storage {ns}:temp _spawn_name
data modify storage {ns}:temp _spawn_label.group_id set from storage {ns}:temp _spawn.group_id
execute store result storage {ns}:temp _spawn_label.sid int 1 run scoreboard players get #zb_spawn_sid {ns}.data
function {ns}:v{version}/zombies/spawn_name with storage {ns}:temp _spawn_label

function {ns}:v{version}/zombies/summon_spawn_at with storage {ns}:temp _spos
execute as @n[type=minecraft:marker,tag={ns}.new_spawn] run function {ns}:v{version}/zombies/spawn_setup

data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter
""")

	write_versioned_function("zombies/spawn_name", f"""
$data modify storage {ns}:temp _spos.name set value "$(name) #$(sid) (group $(group_id))"
""")

	arrival_tags: str = "\n".join(
		f'execute if data storage {ns}:temp _spawn{{arrival:"{arrival}"}} run tag @s add {ns}.arrive_{arrival}' for arrival in ARRIVALS
	)
	## Run as the new marker, its map entry in {ns}:temp _spawn and #sx, #sy, #sz its position.
	write_versioned_function("zombies/spawn_setup", f"""
tag @s remove {ns}.new_spawn
scoreboard players operation @s {ns}.zb.spawn.sid = #zb_spawn_sid {ns}.data
execute store result score @s {ns}.zb.spawn.gid run data get storage {ns}:temp _spawn.group_id

data modify entity @s data.mob set from storage {ns}:temp _spawn.mob
{arrival_tags}
execute store result score @s {ns}.zb.rise_tick run data get storage {ns}:temp _spawn.rise_ticks
execute if score @s {ns}.zb.rise_tick matches ..0 run scoreboard players set @s {ns}.zb.rise_tick 1

# [x, y, z, dx, dy, dz] from the spawn (all 6 needed): only usable while an alive player stands in it (see check_boxes).
execute if data storage {ns}:temp _spawn.activation_box[5] run function {ns}:v{version}/zombies/store_spawn_abox
execute unless data storage {ns}:temp _spawn.activation_box[5] run tag @s add {ns}.spawn_abox_ok

# Enemies of this spawn are escorted to this spot.
execute if data storage {ns}:temp _spawn.walk_to[2] run function {ns}:v{version}/zombies/store_spawn_walk_to

# Bounds are checked at each round start (see check_rounds); max_round 0 never ends.
execute store result score @s {ns}.zb.spawn.rmin run data get storage {ns}:temp _spawn.min_round
execute store result score @s {ns}.zb.spawn.rmax run data get storage {ns}:temp _spawn.max_round
execute if score @s {ns}.zb.spawn.rmin matches ..0 if score @s {ns}.zb.spawn.rmax matches ..0 run tag @s add {ns}.spawn_round_ok
execute unless entity @s[tag={ns}.spawn_round_ok] run tag @s add {ns}.spawn_ranged
execute if score @s {ns}.zb.spawn.rmax matches ..0 run scoreboard players set @s {ns}.zb.spawn.rmax 2147483647

# Switched on with the power (see power/on_activate).
execute store result score #zb_spawn_power {ns}.data run data get storage {ns}:temp _spawn.power
execute unless score #zb_spawn_power {ns}.data matches 1.. run tag @s add {ns}.spawn_powered
""")

	## #sx, #sy, #sz hold the marker position; activation_box[0..2] is the relative corner, [3..5] the size.
	write_versioned_function("zombies/store_spawn_abox", f"""
tag @s add {ns}.spawn_has_abox
execute store result score #abx {ns}.data run data get storage {ns}:temp _spawn.activation_box[0]
execute store result score #aby {ns}.data run data get storage {ns}:temp _spawn.activation_box[1]
execute store result score #abz {ns}.data run data get storage {ns}:temp _spawn.activation_box[2]
scoreboard players operation #abx {ns}.data += #sx {ns}.data
scoreboard players operation #aby {ns}.data += #sy {ns}.data
scoreboard players operation #abz {ns}.data += #sz {ns}.data
execute store result storage {ns}:temp _abox.x double 1 run scoreboard players get #abx {ns}.data
execute store result storage {ns}:temp _abox.y double 1 run scoreboard players get #aby {ns}.data
execute store result storage {ns}:temp _abox.z double 1 run scoreboard players get #abz {ns}.data
execute store result storage {ns}:temp _abox.dx double 1 run data get storage {ns}:temp _spawn.activation_box[3]
execute store result storage {ns}:temp _abox.dy double 1 run data get storage {ns}:temp _spawn.activation_box[4]
execute store result storage {ns}:temp _abox.dz double 1 run data get storage {ns}:temp _spawn.activation_box[5]
data modify entity @s data.abox set from storage {ns}:temp _abox
""")

	## #sx, #sy, #sz hold the marker position, walk_to[0..2] the offset. Three ints, as wander_target and the arrival test expect.
	write_versioned_function("zombies/store_spawn_walk_to", f"""
execute store result score #swx {ns}.data run data get storage {ns}:temp _spawn.walk_to[0]
execute store result score #swy {ns}.data run data get storage {ns}:temp _spawn.walk_to[1]
execute store result score #swz {ns}.data run data get storage {ns}:temp _spawn.walk_to[2]
scoreboard players operation #swx {ns}.data += #sx {ns}.data
scoreboard players operation #swy {ns}.data += #sy {ns}.data
scoreboard players operation #swz {ns}.data += #sz {ns}.data
execute store result storage {ns}:temp _walk_to.x int 1 run scoreboard players get #swx {ns}.data
execute store result storage {ns}:temp _walk_to.y int 1 run scoreboard players get #swy {ns}.data
execute store result storage {ns}:temp _walk_to.z int 1 run scoreboard players get #swz {ns}.data
data modify entity @s data.walk_to set from storage {ns}:temp _walk_to
""")

	## At each round start, before the special round is decided.
	write_versioned_function("zombies/spawns/check_rounds", f"""
tag @e[type=minecraft:marker,tag={ns}.spawn_ranged] remove {ns}.spawn_round_ok
execute as @e[type=minecraft:marker,tag={ns}.spawn_ranged] if score #zb_round {ns}.data >= @s {ns}.zb.spawn.rmin if score #zb_round {ns}.data <= @s {ns}.zb.spawn.rmax run tag @s add {ns}.spawn_round_ok
""")

	## Once a second rather than on every spawn attempt, so a player entering a box opens it within a second.
	write_versioned_function("zombies/spawns/check_boxes", f"""
execute as @e[type=minecraft:marker,tag={ns}.spawn_has_abox,tag={ns}.spawn_unlocked] run function {ns}:v{version}/zombies/spawns/check_box
""")
	write_versioned_function("zombies/spawns/check_box", f"""
tag @s remove {ns}.spawn_abox_ok
function {ns}:v{version}/zombies/spawns/test_box with entity @s data.abox
""")
	write_versioned_function("zombies/spawns/test_box", f"""
$execute if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,x=$(x),y=$(y),z=$(z),dx=$(dx),dy=$(dy),dz=$(dz)] run tag @s add {ns}.spawn_abox_ok
""")
	write_versioned_function("zombies/game_tick", f"""
execute if score #zb_tick_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/spawns/check_boxes
""")

	CoreSpawning.write_summon_spawn_at("zombies", extra_spawn_tags=("new_spawn",))

	CoreSpawning.write_random_spawn_selection("zombies", "spawn_zb_player", "zb.in_game", required_tags=("spawn_unlocked",))

