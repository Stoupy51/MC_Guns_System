""" Spawn markers and picking the one furthest from an enemy. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...core.spawning import CoreSpawning


# Functions
def write_multiplayer_spawns() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Spawn Point Markers.

	## Summon spawn markers from map data (called at game start)
	write_versioned_function("multiplayer/summon_spawns", f"""
# Red spawns
{CoreSpawning.spawn_category_lines("multiplayer", "red", "spawn_red")}

# Blue spawns
{CoreSpawning.spawn_category_lines("multiplayer", "blue", "spawn_blue")}

# General spawns
{CoreSpawning.spawn_category_lines("multiplayer", "general", "spawn_general")}
""")

	CoreSpawning.write_array_spawn_iter("multiplayer")
	CoreSpawning.write_summon_spawn_at("multiplayer")

	# Smart Spawn Selection.

	## TP all players to spawn points at game start
	write_versioned_function("multiplayer/tp_all_to_spawns", f"""
# FFA: everyone uses general spawns
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}

# Team modes: TP by team
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=2}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}

# Players with no team: use general spawns
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=0}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}

# Clean up used spawn markers
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

	## Pick best spawn: find spawn marker farthest from any enemy player (run as player)
	write_versioned_function("multiplayer/pick_spawn", f"""
# Mark this player as needing a spawn
tag @s add {ns}.spawn_pending

# Tag enemy players (for distance calculation — ignore teammates)
# In FFA or team=0: all in-game players are "enemies" for spawn distance
execute if score @s {ns}.mp.team matches 0 run tag @a[scores={{{ns}.mp.in_game=1}}] add {ns}.spawn_enemy
# In team modes: only tag players on different teams
execute if score @s {ns}.mp.team matches 1 run tag @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=2..}}] add {ns}.spawn_enemy
execute if score @s {ns}.mp.team matches 2 run tag @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=..1}}] add {ns}.spawn_enemy
# Never count self as an enemy
tag @s remove {ns}.spawn_enemy

# Tag candidate spawn markers of the right type (exclude already-used spawns). #mp_cand_count
# tracks how many candidates currently carry the tag, so the "all contested" fallback below can
# branch on a score instead of a global @e existence scan. Seed it with the count just tagged.
$execute store result score #mp_cand_count {ns}.data run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_$(type),tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# Remove candidates that have an enemy player within 5 blocks (each removal decrements the count)
execute as @e[tag={ns}.spawn_candidate] at @s if entity @a[tag={ns}.spawn_enemy,distance=..5] run function {ns}:v{version}/multiplayer/uncontest_spawn

# If all were removed (all spawns used or contested), re-tag all as candidates
$execute if score #mp_cand_count {ns}.data matches 0 run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_$(type)] add {ns}.spawn_candidate

# If no enemies, pick random candidate directly (skip expensive distance calc)
execute unless entity @a[tag={ns}.spawn_enemy] run return run function {ns}:v{version}/multiplayer/pick_spawn_random

# Limit to X random candidates before distance computation (optimization)
tag @e[tag={ns}.spawn_candidate,sort=random,limit=32] add {ns}.spawn_final
tag @e[tag={ns}.spawn_candidate,tag=!{ns}.spawn_final] remove {ns}.spawn_candidate
tag @e[tag={ns}.spawn_final] remove {ns}.spawn_final

# Compute distance² to nearest enemy player for each candidate
execute as @e[tag={ns}.spawn_candidate] at @s run function {ns}:v{version}/multiplayer/spawn_calc_dist

# Find the maximum distance score
scoreboard players set #best_dist {ns}.data 0
scoreboard players operation #best_dist {ns}.data > @e[tag={ns}.spawn_candidate] {ns}.data

# Pick the first candidate with that best score and TP the pending player there
execute as @e[tag={ns}.spawn_candidate,sort=random] if score @s {ns}.data = #best_dist {ns}.data run function {ns}:v{version}/shared/tp_to_spawn {{mode:"multiplayer"}}

# Clean up
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
tag @a[tag={ns}.spawn_enemy] remove {ns}.spawn_enemy
""")

	## Drop a contested candidate marker and keep #mp_cand_count in sync (@s = the spawn marker).
	## The tag is always present here (we only iterate spawn_candidate markers), so the decrement is exactly 1:1 with a removal — letting pick_spawn's fallback test a score, not scan @e.
	write_versioned_function("multiplayer/uncontest_spawn", f"""
tag @s remove {ns}.spawn_candidate
scoreboard players remove #mp_cand_count {ns}.data 1
""")

	## Pick random spawn (no enemies — skip distance calc entirely)
	write_versioned_function("multiplayer/pick_spawn_random", f"""
execute as @n[tag={ns}.spawn_candidate,sort=random] run function {ns}:v{version}/shared/tp_to_spawn {{mode:"multiplayer"}}

# Clean up
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
tag @a[tag={ns}.spawn_enemy] remove {ns}.spawn_enemy
""")

	## Calculate distance² from spawn marker to nearest enemy player (run as marker at marker)
	write_versioned_function("multiplayer/spawn_calc_dist", f"""
# Get marker position
execute store result score #mx {ns}.data run data get entity @s Pos[0]
execute store result score #my {ns}.data run data get entity @s Pos[1]
execute store result score #mz {ns}.data run data get entity @s Pos[2]

# Get nearest enemy player position (expensive — caller limits candidates)
data modify storage {ns}:temp _nearest set from entity @p[tag={ns}.spawn_enemy] Pos
execute store result score #px {ns}.data run data get storage {ns}:temp _nearest[0]
execute store result score #py {ns}.data run data get storage {ns}:temp _nearest[1]
execute store result score #pz {ns}.data run data get storage {ns}:temp _nearest[2]

# dx, dy, dz
scoreboard players operation #mx {ns}.data -= #px {ns}.data
scoreboard players operation #my {ns}.data -= #py {ns}.data
scoreboard players operation #mz {ns}.data -= #pz {ns}.data

# distance² = dx² + dy² + dz²
scoreboard players operation #mx {ns}.data *= #mx {ns}.data
scoreboard players operation #my {ns}.data *= #my {ns}.data
scoreboard players operation #mz {ns}.data *= #mz {ns}.data
scoreboard players operation #mx {ns}.data += #my {ns}.data
scoreboard players operation #mx {ns}.data += #mz {ns}.data

# Store on entity
scoreboard players operation @s {ns}.data = #mx {ns}.data
""")

	## Respawn TP: use general spawns on respawn to prevent spawn camping (run as the respawning player)
	write_versioned_function("multiplayer/respawn_tp", f"""
# Try general spawns first (prevents spawn camping)
execute if entity @e[tag={ns}.spawn_point,tag={ns}.spawn_general] run return run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}

# Fallback to team spawns if map has no general spawns
execute if score @s {ns}.mp.team matches 1 run return run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute if score @s {ns}.mp.team matches 2 run return run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}
""")

