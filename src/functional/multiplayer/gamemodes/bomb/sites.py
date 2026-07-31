""" Bomb sites: summoning the marked objectives, and deciding which side defends them.

Shared by Search & Destroy and Demolition because both modes mark the same thing on the map — a chest
under a floating letter — and both have to answer the same question before the first round: which team
already stands next to the objective, since that team is the one that should be defending it.

Every function is written into the *calling variant's* own path (`multiplayer/gamemodes/<key>/...`) and
uses that key for its scratch names, so the two modes stay independent at runtime and the S&D output is
byte-for-byte what it was before this was extracted.
"""
# ruff: noqa: E501
# Imports
from ..base import GameModeVariant


# Classes
class BombSites:
	""" Site markers and side selection, parameterised by the gamemode variant that owns them. """

	# Functions
	@staticmethod
	def setup_lines(variant: GameModeVariant, map_key: str) -> str:
		""" Return the setup lines that read a map's site list and kick off the summon loop.

		Args:
			variant (GameModeVariant): The mode these sites belong to; its key names the scratch storage.
			map_key (str):             Key under `game.map` holding the `[[x, y, z], ...]` site list.
		Returns:
			str: Three commands, one per line.

		Examples:
			>>> BombSites.setup_lines.__doc__ is not None
			True
		"""
		ns, version, key = variant.ns, variant.version, variant.key
		return f"""scoreboard players set #{key}_site_idx {ns}.data 0
data modify storage {ns}:temp _{key}_iter set from storage {ns}:multiplayer game.map.{map_key}
execute if data storage {ns}:temp _{key}_iter[0] run function {ns}:v{version}/multiplayer/gamemodes/{key}/summon_obj"""

	@staticmethod
	def abs_pos_lines(variant: GameModeVariant) -> str:
		""" Return the lines turning `_<key>_iter[0]` (map-relative) into `_<key>_pos` (absolute).

		Shared by the site loop and by Demolition's one-off overtime site, which needs the same conversion
		for a position that does not come from a list.
		"""
		ns, key = variant.ns, variant.key
		return f"""execute store result score #rx {ns}.data run data get storage {ns}:temp _{key}_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _{key}_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _{key}_iter[0][2]
scoreboard players operation #rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _{key}_pos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _{key}_pos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _{key}_pos.z double 1 run scoreboard players get #rz {ns}.data"""

	@staticmethod
	def write_summoning(variant: GameModeVariant) -> None:
		""" Write `summon_obj` + `summon_obj_at`: the relative → absolute loop and the marker itself. """
		ns, version, key = variant.ns, variant.version, variant.key

		## Summon objective markers (relative → absolute)
		variant.sub("summon_obj", f"""
{BombSites.abs_pos_lines(variant)}

# Site letter, same scheme as domination's zone labels
execute if score #{key}_site_idx {ns}.data matches 0 run data modify storage {ns}:temp _{key}_pos.label set value "A"
execute if score #{key}_site_idx {ns}.data matches 1 run data modify storage {ns}:temp _{key}_pos.label set value "B"
execute if score #{key}_site_idx {ns}.data matches 2 run data modify storage {ns}:temp _{key}_pos.label set value "C"
execute if score #{key}_site_idx {ns}.data matches 3 run data modify storage {ns}:temp _{key}_pos.label set value "D"
scoreboard players add #{key}_site_idx {ns}.data 1

function {ns}:v{version}/multiplayer/gamemodes/{key}/summon_obj_at with storage {ns}:temp _{key}_pos
data remove storage {ns}:temp _{key}_iter[0]
execute if data storage {ns}:temp _{key}_iter[0] run function {ns}:v{version}/multiplayer/gamemodes/{key}/summon_obj
""")

		## The floating letter is what domination has and S&D did not: without it the sites are an unmarked
		## chest, so neither side can tell where the objective is without being told out of band. The letter
		## also names the site in chat when the bomb goes down there, which is how defenders rotate.
		variant.sub("summon_obj_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.{key}_obj","{ns}.gm_entity","{ns}.{key}_site_$(label)"]}}
$summon minecraft:text_display $(x) $(y) $(z) {{Tags:["{ns}.{key}_label","{ns}.gm_entity"],billboard:"vertical",text:[{{"text":"💣 ","color":"gold"}},{{"text":"$(label)","color":"yellow","bold":true}}],transformation:{{translation:[0.0f,2.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[3.0f,3.0f,3.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}
$execute positioned $(x) $(y) $(z) run setblock ~ ~ ~ chest
$execute positioned $(x) $(y) $(z) run setblock ~ ~1 ~ barrier
""")

	@staticmethod
	def write_side_picking(variant: GameModeVariant) -> None:
		""" Write `pick_sides` + the two tally helpers: the defenders are whoever spawns next to the sites. """
		ns, version, key = variant.ns, variant.version, variant.key

		## Choose which side defends — whoever spawns closest to the bomb sites.
		## Hardcoding Red as attackers put the attackers on top of the objective on roughly half of all
		## maps, which removes the entire point of the mode: the defenders are supposed to hold ground they
		## start next to, and the attackers are supposed to cross the map to reach it.
		variant.sub("pick_sides", f"""
# Tally, per bomb site, which team owns the spawn point closest to it.
scoreboard players set #{key}_near_red {ns}.data 0
scoreboard players set #{key}_near_blue {ns}.data 0
execute as @e[tag={ns}.{key}_obj] at @s run function {ns}:v{version}/multiplayer/gamemodes/{key}/tally_site

# Attackers are whichever side did NOT win that tally. A tie keeps Red attacking, the CoD default.
scoreboard players set #{key}_attackers {ns}.data 1
execute if score #{key}_near_red {ns}.data > #{key}_near_blue {ns}.data run scoreboard players set #{key}_attackers {ns}.data 2
""")

		## @s = one bomb site, at it. Credit the site to the team owning the nearest spawn point.
		## General spawns are excluded: they say nothing about which side holds this ground.
		variant.sub("tally_site", f"""
execute as @e[tag={ns}.spawn_point,tag=!{ns}.spawn_general,limit=1,sort=nearest] run function {ns}:v{version}/multiplayer/gamemodes/{key}/tally_site_spawn
""")

		variant.sub("tally_site_spawn", f"""
execute if entity @s[tag={ns}.spawn_red] run scoreboard players add #{key}_near_red {ns}.data 1
execute if entity @s[tag={ns}.spawn_blue] run scoreboard players add #{key}_near_blue {ns}.data 1
""")

	@staticmethod
	def cleanup_lines(variant: GameModeVariant) -> str:
		""" Return the lines that restore the world where the sites were and remove their entities.

		The `fill` has to run while the markers are still alive, which is why every mode's `cleanup` runs
		before `multiplayer/stop` sweeps `gm_entity` (see game/stop.py).
		"""
		ns, key = variant.ns, variant.key
		return f"""execute at @e[tag={ns}.{key}_obj] run fill ~ ~ ~ ~ ~1 ~ air
kill @e[tag={ns}.{key}_obj]
kill @e[tag={ns}.{key}_label]"""
