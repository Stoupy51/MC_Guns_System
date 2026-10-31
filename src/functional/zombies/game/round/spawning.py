""" Spawn pacing, and picking an open spawn near the players to bring an enemy in. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..lifecycle.spawns import ENEMY_SPAWNS, open_spawn


# Functions
def write_round_spawning() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Spawn timer max(1, 20 - round) ticks, batch floor((round - 1) / 50) + 1.
	write_versioned_function("zombies/calc_spawn_timer", f"""
scoreboard players set #zb_spawn_timer {ns}.data 20
scoreboard players operation #zb_spawn_timer {ns}.data -= #zb_round {ns}.data
execute if score #zb_spawn_timer {ns}.data matches ..1 run scoreboard players set #zb_spawn_timer {ns}.data 1

scoreboard players operation #zb_spawn_batch {ns}.data = #zb_round {ns}.data
scoreboard players remove #zb_spawn_batch {ns}.data 1
scoreboard players operation #zb_spawn_batch {ns}.data /= #50 {ns}.data
scoreboard players add #zb_spawn_batch {ns}.data 1

# Special rounds pace on the concurrency cap of spawn_special_capped, not on the zombie curve,
# which reaches 1 tick by round 20 and would release a whole pack in one second.
execute if score #zb_special_round {ns}.data matches 1 run scoreboard players set #zb_spawn_timer {ns}.data 20
execute if score #zb_special_round {ns}.data matches 1 run scoreboard players set #zb_spawn_batch {ns}.data 1
""")

	for kind in ENEMY_SPAWNS:
		marker: str = f"{open_spawn(ns)},tag={ns}.{kind.tag}"

		# Tag the open spawns of this kind closest to any alive player (within 32, else 64, else any); callers leave zb_near empty.
		# Each player's pass adds what it tagged to #zb_near_found, since `store` on an `as @a` line keeps only the last iteration.
		write_versioned_function(f"zombies/tag_{kind.key}_spawns_near_players", f"""
scoreboard players set #zb_near_found {ns}.data 0

execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/tag_{kind.key}_near_32

execute if score #zb_near_found {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/tag_{kind.key}_near_64

# `store success` so #zb_near_found also reflects the fallback.
execute if score #zb_near_found {ns}.data matches 0 store success score #zb_near_found {ns}.data run tag @e[{marker}] add {ns}.zb_near
""")

		## Run as an alive in-game player, at their position.
		for radius in (32, 64):
			write_versioned_function(f"zombies/tag_{kind.key}_near_{radius}", f"""
execute store result score #zb_near_hit {ns}.data run tag @e[{marker},distance=..{radius}] add {ns}.zb_near
scoreboard players operation #zb_near_found {ns}.data += #zb_near_hit {ns}.data
""")

		## One enemy at an open spawn of this kind near a player; #zb_spawned is 0 when none is open.
		write_versioned_function(f"zombies/spawn_from/{kind.key}", f"""
scoreboard players set #zb_spawned {ns}.data 0
function {ns}:v{version}/zombies/tag_{kind.key}_spawns_near_players
execute as @n[type=minecraft:marker,tag={ns}.zb_near,sort=random] at @s run function {ns}:v{version}/zombies/do_spawn
tag @e[type=minecraft:marker,tag={ns}.zb_near] remove {ns}.zb_near
""")

	## Run as the spawn marker, at it.
	write_versioned_function("zombies/do_spawn", f"""
scoreboard players set #zb_spawned {ns}.data 1
data modify storage {ns}:temp _mob set from entity @s data.mob
scoreboard players operation #zb_spawn_sid {ns}.data = @s {ns}.zb.spawn.sid
execute store result score #zb_spawn_x {ns}.data run data get entity @s Pos[0]
execute store result score #zb_spawn_z {ns}.data run data get entity @s Pos[2]

execute if entity @s[tag={ns}.arrive_portal] run return run function {ns}:v{version}/zombies/arrival/portal
execute if entity @s[tag={ns}.arrive_instant] run return run function {ns}:v{version}/zombies/arrival/instant
execute if entity @s[tag={ns}.arrive_ceiling] run return run function {ns}:v{version}/zombies/arrival/ceiling
function {ns}:v{version}/zombies/arrival/floor
""")

	## Release one enemy unless the pack is full; a skipped spawn stays queued in #zb_to_spawn.
	write_versioned_function("zombies/spawn_special_capped", f"""
scoreboard players operation #zb_special_live {ns}.data = #zb_alive {ns}.data
scoreboard players operation #zb_special_live {ns}.data += #zb_portal_pending {ns}.data
execute if score #zb_special_live {ns}.data >= #zb_special_cap {ns}.data run return 0

function {ns}:v{version}/zombies/spawn_from/special
execute if score #zb_spawned {ns}.data matches 1 run scoreboard players remove #zb_to_spawn {ns}.data 1
""")

