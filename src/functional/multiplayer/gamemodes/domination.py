
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG


def generate_domination() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## DOM Setup: Summon capture point markers from loaded map
	write_versioned_function("multiplayer/gamemodes/dom/setup", f"""
tellraw @a [{MGS_TAG},{{"text":"Domination! Capture and hold zones to earn points!","color":"yellow"}}]

# Store base coordinates for offset computation
execute store result score #gm_base_x {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[0]
execute store result score #gm_base_y {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[1]
execute store result score #gm_base_z {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[2]

# Summon capture point markers from relative coords
data modify storage {ns}:temp _dom_iter set from storage {ns}:multiplayer game.map.domination
execute if data storage {ns}:temp _dom_iter[0] run function {ns}:v{version}/multiplayer/gamemodes/dom/summon_point

# Initialize scoring interval timer (score every 5 seconds = 100 ticks)
scoreboard players set #dom_score_timer {ns}.data 100
""")

	## DOM: Summon a single capture point marker (convert relative to absolute)
	write_versioned_function("multiplayer/gamemodes/dom/summon_point", f"""
# Read relative coords
execute store result score #_rx {ns}.data run data get storage {ns}:temp _dom_iter[0][0]
execute store result score #_ry {ns}.data run data get storage {ns}:temp _dom_iter[0][1]
execute store result score #_rz {ns}.data run data get storage {ns}:temp _dom_iter[0][2]

# Add base offset
scoreboard players operation #_rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_rz {ns}.data += #gm_base_z {ns}.data

# Prepare position for macro
execute store result storage {ns}:temp _dom_pos.x double 1 run scoreboard players get #_rx {ns}.data
execute store result storage {ns}:temp _dom_pos.y double 1 run scoreboard players get #_ry {ns}.data
execute store result storage {ns}:temp _dom_pos.z double 1 run scoreboard players get #_rz {ns}.data

# Summon
function {ns}:v{version}/multiplayer/gamemodes/dom/summon_point_at with storage {ns}:temp _dom_pos

# Advance
data remove storage {ns}:temp _dom_iter[0]
execute if data storage {ns}:temp _dom_iter[0] run function {ns}:v{version}/multiplayer/gamemodes/dom/summon_point
""")

	## DOM: Summon marker at computed absolute coords (macro)
	write_versioned_function("multiplayer/gamemodes/dom/summon_point_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.dom_point","{ns}.gm_entity"]}}
""")

	## DOM Tick: Check capture progress + score
	write_versioned_function("multiplayer/gamemodes/dom/tick", f"""
# Process each domination point
execute as @e[tag={ns}.dom_point] at @s run function {ns}:v{version}/multiplayer/gamemodes/dom/point_tick

# Scoring interval
scoreboard players remove #dom_score_timer {ns}.data 1
execute if score #dom_score_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/dom/score_tick
execute if score #dom_score_timer {ns}.data matches ..0 run scoreboard players set #dom_score_timer {ns}.data 100

# Show particles at each point
execute as @e[tag={ns}.dom_point] at @s run function {ns}:v{version}/multiplayer/gamemodes/dom/point_particles
""")

	## DOM: Per-point tick - check nearby players and adjust capture
	write_versioned_function("multiplayer/gamemodes/dom/point_tick", f"""
# Count red and blue players within 5 blocks
execute store result score #_dom_red {ns}.data if entity @a[distance=..5,scores={{{ns}.mp.team=1}}]
execute store result score #_dom_blue {ns}.data if entity @a[distance=..5,scores={{{ns}.mp.team=2}}]

# If contested (both teams present), no progress change
execute if score #_dom_red {ns}.data matches 1.. if score #_dom_blue {ns}.data matches 1.. run return fail

# If only red present: progress toward red (increase toward 100)
execute if score #_dom_red {ns}.data matches 1.. unless score #_dom_blue {ns}.data matches 1.. run function {ns}:v{version}/multiplayer/gamemodes/dom/capture_red

# If only blue present: progress toward blue (decrease toward -100)
execute if score #_dom_blue {ns}.data matches 1.. unless score #_dom_red {ns}.data matches 1.. run function {ns}:v{version}/multiplayer/gamemodes/dom/capture_blue
""")

	## DOM: Capture for red (progress goes +)
	write_versioned_function("multiplayer/gamemodes/dom/capture_red", f"""
# Get current progress
execute store result score #_dom_prog {ns}.data run scoreboard players get @s {ns}.mp.dom_progress

# Increase progress (2 per tick when capturing)
scoreboard players add @s {ns}.mp.dom_progress 2

# Cap at 100
execute if score @s {ns}.mp.dom_progress matches 101.. run scoreboard players set @s {ns}.mp.dom_progress 100

# If crossed 0 from negative (was blue, now contested), briefly neutral
execute if score #_dom_prog {ns}.data matches ..-1 if score @s {ns}.mp.dom_progress matches 0.. run scoreboard players set @s {ns}.mp.dom_owner 0
execute if score #_dom_prog {ns}.data matches ..-1 if score @s {ns}.mp.dom_progress matches 0.. run tellraw @a [{MGS_TAG},{{"text":"Domination point neutralized!","color":"yellow"}}]

# If reached 100, captured by red
execute if score @s {ns}.mp.dom_progress matches 100 unless score @s {ns}.mp.dom_owner matches 1 run scoreboard players set @s {ns}.mp.dom_owner 1
execute if score @s {ns}.mp.dom_progress matches 100 unless score @s {ns}.mp.dom_owner matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" captured a point!","color":"yellow"}}]
""")

	## DOM: Capture for blue (progress goes -)
	write_versioned_function("multiplayer/gamemodes/dom/capture_blue", f"""
# Decrease progress (2 per tick when capturing)
execute store result score #_dom_prog {ns}.data run scoreboard players get @s {ns}.mp.dom_progress
scoreboard players remove @s {ns}.mp.dom_progress 2

# Cap at -100
execute if score @s {ns}.mp.dom_progress matches ..-101 run scoreboard players set @s {ns}.mp.dom_progress -100

# If crossed 0 from positive (was red, now contested)
execute if score #_dom_prog {ns}.data matches 1.. if score @s {ns}.mp.dom_progress matches ..0 run scoreboard players set @s {ns}.mp.dom_owner 0
execute if score #_dom_prog {ns}.data matches 1.. if score @s {ns}.mp.dom_progress matches ..0 run tellraw @a [{MGS_TAG},{{"text":"Domination point neutralized!","color":"yellow"}}]

# If reached -100, captured by blue
execute if score @s {ns}.mp.dom_progress matches -100 unless score @s {ns}.mp.dom_owner matches 2 run scoreboard players set @s {ns}.mp.dom_owner 2
execute if score @s {ns}.mp.dom_progress matches -100 unless score @s {ns}.mp.dom_owner matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" captured a point!","color":"yellow"}}]
""")

	## DOM: Score tick - +1 per owned point
	write_versioned_function("multiplayer/gamemodes/dom/score_tick", f"""
# Count red-owned and blue-owned points
execute store result score #_dom_r {ns}.data if entity @e[tag={ns}.dom_point,scores={{{ns}.mp.dom_owner=1}}]
execute store result score #_dom_b {ns}.data if entity @e[tag={ns}.dom_point,scores={{{ns}.mp.dom_owner=2}}]

# Add to team scores
scoreboard players operation #red {ns}.mp.team += #_dom_r {ns}.data
scoreboard players operation #blue {ns}.mp.team += #_dom_b {ns}.data

# Check win
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score #red {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
""")

	## DOM: Point particles (colored by owner)
	write_versioned_function("multiplayer/gamemodes/dom/point_particles", f"""
# Neutral = white, red = red, blue = blue
execute if score @s {ns}.mp.dom_owner matches 0 run particle dust{{color:[1.0,1.0,1.0],scale:1.0}} ~ ~1 ~ 1.5 0.5 1.5 0 5
execute if score @s {ns}.mp.dom_owner matches 1 run particle dust{{color:[1.0,0.2,0.2],scale:1.0}} ~ ~1 ~ 1.5 0.5 1.5 0 5
execute if score @s {ns}.mp.dom_owner matches 2 run particle dust{{color:[0.2,0.2,1.0],scale:1.0}} ~ ~1 ~ 1.5 0.5 1.5 0 5
""")

	## DOM Kill Hook: Kills also give +1 to team
	write_versioned_function("multiplayer/gamemodes/dom/on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
execute if score @s {ns}.mp.team matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players add #blue {ns}.mp.team 1
""")

	## DOM Cleanup: Kill markers
	write_versioned_function("multiplayer/gamemodes/dom/cleanup", f"""
kill @e[tag={ns}.dom_point]
""")
