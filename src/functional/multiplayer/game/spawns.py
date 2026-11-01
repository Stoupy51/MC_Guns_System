""" Spawn markers and picking the one furthest from an enemy. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...core.spawning import CoreSpawning
from ...helpers.probes import Probe


# Functions
def write_multiplayer_spawns() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Run at game start.
	write_versioned_function("multiplayer/summon_spawns", f"""
{CoreSpawning.spawn_category_lines("multiplayer", "red", "spawn_red")}

{CoreSpawning.spawn_category_lines("multiplayer", "blue", "spawn_blue")}

{CoreSpawning.spawn_category_lines("multiplayer", "general", "spawn_general")}
""")

	CoreSpawning.write_array_spawn_iter("multiplayer")
	CoreSpawning.write_summon_spawn_at("multiplayer")

	write_versioned_function("multiplayer/tp_all_to_spawns", f"""
# FFA: everyone uses general spawns.
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}

execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=2}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}

# No team: general spawns.
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=0}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}

tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

	## Run as the player: the candidate spawn farthest from any enemy.
	write_versioned_function("multiplayer/pick_spawn", f"""
tag @s add {ns}.spawn_pending

# FFA or team 0: every other in-game player is an enemy.
execute if score @s {ns}.mp.team matches 0 run tag @a[scores={{{ns}.mp.in_game=1}}] add {ns}.spawn_enemy
# Team modes: only the other team.
execute if score @s {ns}.mp.team matches 1 run tag @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=2..}}] add {ns}.spawn_enemy
execute if score @s {ns}.mp.team matches 2 run tag @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=..1}}] add {ns}.spawn_enemy
tag @s remove {ns}.spawn_enemy

# #mp_cand_count follows the tagged candidates, so the "all contested" fallback tests a score instead of scanning @e.
$execute store result score #mp_cand_count {ns}.data run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_$(type),tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# Drop candidates with an enemy within 5 blocks.
execute as @e[tag={ns}.spawn_candidate] at @s if entity @a[tag={ns}.spawn_enemy,distance=..5] run function {ns}:v{version}/multiplayer/uncontest_spawn

# All used or contested: every spawn of the type is a candidate again.
$execute if score #mp_cand_count {ns}.data matches 0 run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_$(type)] add {ns}.spawn_candidate

# No enemies: any candidate, without the distance computation.
execute unless entity @a[tag={ns}.spawn_enemy] run return run function {ns}:v{version}/multiplayer/pick_spawn_random

# At most 32 random candidates get the distance computation.
tag @e[tag={ns}.spawn_candidate,sort=random,limit=32] add {ns}.spawn_final
tag @e[tag={ns}.spawn_candidate,tag=!{ns}.spawn_final] remove {ns}.spawn_candidate
tag @e[tag={ns}.spawn_final] remove {ns}.spawn_final

# Squared distance to the nearest enemy.
execute as @e[tag={ns}.spawn_candidate] at @s run function {ns}:v{version}/multiplayer/spawn_calc_dist

scoreboard players set #best_dist {ns}.data 0
scoreboard players operation #best_dist {ns}.data > @e[tag={ns}.spawn_candidate] {ns}.data

# A random one among the farthest.
execute as @e[tag={ns}.spawn_candidate,sort=random] if score @s {ns}.data = #best_dist {ns}.data run function {ns}:v{version}/shared/tp_to_spawn {{mode:"multiplayer"}}

tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
tag @a[tag={ns}.spawn_enemy] remove {ns}.spawn_enemy
""")

	## Run as a candidate marker; the tag is always present here, so the count drops exactly once per removal.
	write_versioned_function("multiplayer/uncontest_spawn", f"""
tag @s remove {ns}.spawn_candidate
scoreboard players remove #mp_cand_count {ns}.data 1
""")

	write_versioned_function("multiplayer/pick_spawn_random", f"""
execute as @n[tag={ns}.spawn_candidate,sort=random] run function {ns}:v{version}/shared/tp_to_spawn {{mode:"multiplayer"}}

tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
tag @a[tag={ns}.spawn_enemy] remove {ns}.spawn_enemy
""")

	## Run as the marker, at it.
	enemy: str = f"@p[tag={ns}.spawn_enemy]"
	write_versioned_function("multiplayer/spawn_calc_dist", f"""
execute store result score #mx {ns}.data run data get entity @s Pos[0]
execute store result score #my {ns}.data run data get entity @s Pos[1]
execute store result score #mz {ns}.data run data get entity @s Pos[2]

# The caller limits the candidate set.
{Probe.pos(enemy)}
execute store result score #px {ns}.data run data get storage {ns}:temp _probe_pos[0]
execute store result score #py {ns}.data run data get storage {ns}:temp _probe_pos[1]
execute store result score #pz {ns}.data run data get storage {ns}:temp _probe_pos[2]

scoreboard players operation #mx {ns}.data -= #px {ns}.data
scoreboard players operation #my {ns}.data -= #py {ns}.data
scoreboard players operation #mz {ns}.data -= #pz {ns}.data

scoreboard players operation #mx {ns}.data *= #mx {ns}.data
scoreboard players operation #my {ns}.data *= #my {ns}.data
scoreboard players operation #mz {ns}.data *= #mz {ns}.data
scoreboard players operation #mx {ns}.data += #my {ns}.data
scoreboard players operation #mx {ns}.data += #mz {ns}.data

scoreboard players operation @s {ns}.data = #mx {ns}.data
""")

	## Run as the respawning player.
	write_versioned_function("multiplayer/respawn_tp", f"""
# General spawns first, against spawn camping.
execute if entity @e[tag={ns}.spawn_point,tag={ns}.spawn_general] run return run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}

# Team spawns when the map has no general ones.
execute if score @s {ns}.mp.team matches 1 run return run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute if score @s {ns}.mp.team matches 2 run return run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}
""")

