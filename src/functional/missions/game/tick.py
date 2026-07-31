""" The game tick, the compass pointing at the nearest enemy and the victory check. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_tick_file, write_versioned_function

from ...core.respawn_countdown import respawn_countdown_tick_lines
from ...core.weapon_drop import WeaponDrop
from ...helpers.text import Text
from ...helpers.titles import TitleTimes


# Functions
def write_missions_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Game Tick
	write_tick_file(f"""
# Missions game tick
execute if data storage {ns}:missions game{{state:"active"}} run function {ns}:v{version}/missions/game_tick
execute if data storage {ns}:missions game{{state:"preparing"}} run function {ns}:v{version}/missions/prep_tick
""")

	write_versioned_function("missions/game_tick", f"""
{respawn_countdown_tick_lines(ns, "mi", f"{ns}:v{version}/missions/actual_respawn")}

# Increment mission timer
scoreboard players operation #mi_timer {ns}.data += #tick_delta {ns}.data

# Boundary enforcement (skip spectators) & OOB Check
execute if score #mi_has_boundary {ns}.data matches 1 as @e[tag={ns}.mission_enemy] at @s run function {ns}:v{version}/shared/check_bounds
execute if score #mi_has_boundary {ns}.data matches 1 as @e[type=player,scores={{{ns}.mi.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/shared/check_bounds
execute as @e[type=player,scores={{{ns}.mi.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag={ns}.oob_point,distance=..5] run damage @s 10000 out_of_world

# Enemies drop their weapon at the corpse; the drops then live for 30s
function {ns}:v{version}/missions/death_watch_tick
{WeaponDrop.weapon_drop_tick_lines(ns)}

# Track enemy kills (total enemies - alive enemies)
execute store result score #alive {ns}.data if entity @e[tag={ns}.mission_enemy]
scoreboard players operation #mi_kills {ns}.data = #mi_total_enemies {ns}.data
scoreboard players operation #mi_kills {ns}.data -= #alive {ns}.data

# Update compass for all players every 10 ticks (points to nearest enemy — each update is an
# item write + macro parse per player, and a lodestone compass doesn't need 20Hz retargeting)
scoreboard players operation #mi_compass_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #mi_compass_phase {ns}.data %= #10 {ns}.data
execute if score #alive {ns}.data matches 1.. if score #mi_compass_phase {ns}.data matches 0 as @a[scores={{{ns}.mi.in_game=1}}] at @s run function {ns}:v{version}/missions/update_compass

# Orb cleanup around any one in-game player (@r paid a random sort every tick for nothing)
execute at @a[scores={{{ns}.mi.in_game=1}},limit=1] run kill @e[type=experience_orb,distance=..200]

# Call map-defined tick script
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"tick"}}

# Check if all enemies are dead → victory (reuses #alive counted above instead of a second
# full-entity scan; a kill from the map tick script above is caught one tick later).
# Requires at least one spawned enemy so a broken spawn can never instantly end the game.
execute if score #mi_total_enemies {ns}.data matches 1.. if score #alive {ns}.data matches 0 run return run function {ns}:v{version}/missions/victory
""")

	## Compass pointing at the nearest enemy, run as the player at the player.
	## The caller guarantees #alive >= 1, so no per-player emptiness rescan is needed.
	write_versioned_function("missions/update_compass", f"""
# Only players actually carrying the mission compass need the item write
execute unless items entity @s hotbar.3 minecraft:compass run return fail

# Get nearest enemy position: ONE sorted scan + ONE NBT read, then cheap storage extracts
# (was three @n scans, each with its own distance sort and Pos read)
data modify storage {ns}:temp _compass.pos set from entity @n[tag={ns}.mission_enemy] Pos
execute store result storage {ns}:temp _compass.x int 1 run data get storage {ns}:temp _compass.pos[0]
execute store result storage {ns}:temp _compass.y int 1 run data get storage {ns}:temp _compass.pos[1]
execute store result storage {ns}:temp _compass.z int 1 run data get storage {ns}:temp _compass.pos[2]

# Update compass in hotbar slot 3
function {ns}:v{version}/missions/set_compass_target with storage {ns}:temp _compass
""")

	write_versioned_function("missions/set_compass_target", f"""
$item replace entity @s hotbar.3 with compass[lodestone_tracker={{target:{{pos:[I;$(x),$(y),$(z)],dimension:"minecraft:overworld"}},tracked:false}},custom_data={{{ns}:{{compass:true}}}}]
""")

	## Victory - all enemies killed!
	write_versioned_function("missions/victory", f"""
# Compute per-player mission kills from totalKillCount delta
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mi.kills = @s {ns}.mi.kill_total
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mi.kills -= @s {ns}.mi.kill_base

# Calculate time in seconds
scoreboard players operation #mi_seconds {ns}.data = #mi_timer {ns}.data
scoreboard players operation #mi_seconds {ns}.data /= #20 {ns}.data

# Calculate minutes and remaining seconds
scoreboard players operation #mi_minutes {ns}.data = #mi_seconds {ns}.data
scoreboard players operation #mi_minutes {ns}.data /= #60 {ns}.data
scoreboard players operation #mi_rem_sec {ns}.data = #mi_seconds {ns}.data
scoreboard players operation #mi_rem_sec {ns}.data %= #60 {ns}.data

# Title
{TitleTimes.BANNER.cmd(f'@a[scores={{{ns}.mi.in_game=1}}]')}
title @a[scores={{{ns}.mi.in_game=1}}] title {{"text":"MISSION COMPLETE","color":"gold","bold":true}}
title @a[scores={{{ns}.mi.in_game=1}}] subtitle {{"text":"All enemies eliminated!","color":"green"}}

# Performance summary
tellraw @a ["","\\n",{{"text":"═══════ MISSION COMPLETE ═══════","color":"gold","bold":true}}]
tellraw @a ["","  ","⏱ ",{{"text":"Time: ","color":"gray"}},{{"score":{{"name":"#mi_minutes","objective":"{ns}.data"}},"color":"yellow"}},"m ",{{"score":{{"name":"#mi_rem_sec","objective":"{ns}.data"}},"color":"yellow"}},"s"]
tellraw @a ["","  ","💀 ",{{"text":"Enemies killed: ","color":"gray"}},{{"score":{{"name":"#mi_total_enemies","objective":"{ns}.data"}},"color":"red"}}]

# Per-player stats
execute as @a[scores={{{ns}.mi.in_game=1}}] run tellraw @a ["","  ","🎖 ",{Text.player(ns, "@s", color="yellow")}," — Kills: ",{{"score":{{"name":"@s","objective":"{ns}.mi.kills"}},"color":"green"}}," | Deaths: ",{{"score":{{"name":"@s","objective":"{ns}.mi.deaths"}},"color":"red"}}]

tellraw @a ["",{{"text":"═══════════════════════════════","color":"gold","bold":true}},"\\n"]

# End game
function {ns}:v{version}/missions/stop
""")

