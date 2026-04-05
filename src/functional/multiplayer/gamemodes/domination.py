
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
function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

# Initialize zone counter for labeling (A, B, C...)
scoreboard players set #dom_zone_idx {ns}.data 0

# Initialize global point ownership scores (0=neutral, 1=red, 2=blue)
scoreboard players set #dom_owner_a {ns}.data 0
scoreboard players set #dom_owner_b {ns}.data 0
scoreboard players set #dom_owner_c {ns}.data 0
scoreboard players set #dom_owner_d {ns}.data 0
scoreboard players set #dom_owner_e {ns}.data 0

# Store total number of points for sidebar
scoreboard players set #dom_point_count {ns}.data 0

# Summon capture point markers from relative coords
data modify storage {ns}:temp _dom_iter set from storage {ns}:multiplayer game.map.domination
execute if data storage {ns}:temp _dom_iter[0] run function {ns}:v{version}/multiplayer/gamemodes/dom/summon_point

# Store final count of dom points
execute store result score #dom_point_count {ns}.data if entity @e[tag={ns}.dom_point]

# Initialize scoring interval timer (score every 5 seconds = 100 ticks)
scoreboard players set #dom_score_timer {ns}.data 100
""")

	## DOM: Summon a single capture point marker (convert relative to absolute)
	write_versioned_function("multiplayer/gamemodes/dom/summon_point", f"""
# Read relative coords
execute store result score #rx {ns}.data run data get storage {ns}:temp _dom_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _dom_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _dom_iter[0][2]

# Add base offset
scoreboard players operation #rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #rz {ns}.data += #gm_base_z {ns}.data

# Prepare position for macro
execute store result storage {ns}:temp _dom_pos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _dom_pos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _dom_pos.z double 1 run scoreboard players get #rz {ns}.data

# Assign zone label (A, B, C, D, E)
execute if score #dom_zone_idx {ns}.data matches 0 run data modify storage {ns}:temp _dom_pos.label set value "A"
execute if score #dom_zone_idx {ns}.data matches 1 run data modify storage {ns}:temp _dom_pos.label set value "B"
execute if score #dom_zone_idx {ns}.data matches 2 run data modify storage {ns}:temp _dom_pos.label set value "C"
execute if score #dom_zone_idx {ns}.data matches 3 run data modify storage {ns}:temp _dom_pos.label set value "D"
execute if score #dom_zone_idx {ns}.data matches 4 run data modify storage {ns}:temp _dom_pos.label set value "E"
scoreboard players add #dom_zone_idx {ns}.data 1

# Summon marker + text label
function {ns}:v{version}/multiplayer/gamemodes/dom/summon_point_at with storage {ns}:temp _dom_pos

# Advance
data remove storage {ns}:temp _dom_iter[0]
execute if data storage {ns}:temp _dom_iter[0] run function {ns}:v{version}/multiplayer/gamemodes/dom/summon_point
""")

	## DOM: Summon marker + text label at computed absolute coords (macro)
	write_versioned_function("multiplayer/gamemodes/dom/summon_point_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.dom_point","{ns}.gm_entity","{ns}.dom_label_$(label)"]}}
$summon minecraft:text_display $(x) $(y) $(z) {{Tags:["{ns}.dom_label","{ns}.gm_entity","{ns}.dom_$(label)"],billboard:"vertical",text:{{"text":"$(label)","color":"yellow","bold":true}},transformation:{{translation:[0.0f,2.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[3.0f,3.0f,3.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}
""")

	## DOM Tick: Check capture progress + score
	write_versioned_function("multiplayer/gamemodes/dom/tick", f"""
# Process each domination point
execute as @e[tag={ns}.dom_point] at @s run function {ns}:v{version}/multiplayer/gamemodes/dom/point_tick

# Sync point ownership to global scores for sidebar display
execute as @e[tag={ns}.dom_point,tag={ns}.dom_label_A] store result score #dom_owner_a {ns}.data run scoreboard players get @s {ns}.mp.dom_owner
execute as @e[tag={ns}.dom_point,tag={ns}.dom_label_B] store result score #dom_owner_b {ns}.data run scoreboard players get @s {ns}.mp.dom_owner
execute as @e[tag={ns}.dom_point,tag={ns}.dom_label_C] store result score #dom_owner_c {ns}.data run scoreboard players get @s {ns}.mp.dom_owner
execute as @e[tag={ns}.dom_point,tag={ns}.dom_label_D] store result score #dom_owner_d {ns}.data run scoreboard players get @s {ns}.mp.dom_owner
execute as @e[tag={ns}.dom_point,tag={ns}.dom_label_E] store result score #dom_owner_e {ns}.data run scoreboard players get @s {ns}.mp.dom_owner

# Scoring interval
scoreboard players remove #dom_score_timer {ns}.data 1
execute if score #dom_score_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/dom/score_tick
execute if score #dom_score_timer {ns}.data matches ..0 run scoreboard players set #dom_score_timer {ns}.data 100

# Show particles at each point
execute as @e[tag={ns}.dom_point] at @s run function {ns}:v{version}/multiplayer/gamemodes/dom/point_particles
""")

	## DOM: Per-point tick - check nearby players and adjust capture
	write_versioned_function("multiplayer/gamemodes/dom/point_tick", f"""
# Visual capture progress particles (smooth blue <-> yellow <-> red gradient)
execute if score @s {ns}.mp.dom_progress matches -65..65 run particle dust{{color:[1.0,1.0,0.0],scale:1.0}} ~ ~1 ~ 1 1 1 0 5
execute if score @s {ns}.mp.dom_progress matches 34..65 run particle dust{{color:[1.0,0.75,0.25],scale:1.0}} ~ ~1 ~ 1 1 1 0 5
execute if score @s {ns}.mp.dom_progress matches 66..99 run particle dust{{color:[1.0,0.5,0.0],scale:1.0}} ~ ~1 ~ 1 1 1 0 5
execute if score @s {ns}.mp.dom_progress matches 100 run particle dust{{color:[1.0,0.0,0.0],scale:1.0}} ~ ~1 ~ 1 1 1 0 5
execute if score @s {ns}.mp.dom_progress matches -65..-34 run particle dust{{color:[0.25,0.75,1.0],scale:1.0}} ~ ~1 ~ 1 1 1 0 5
execute if score @s {ns}.mp.dom_progress matches -99..-66 run particle dust{{color:[0.0,0.5,1.0],scale:1.0}} ~ ~1 ~ 1 1 1 0 5
execute if score @s {ns}.mp.dom_progress matches -100 run particle dust{{color:[0.0,0.0,1.0],scale:1.0}} ~ ~1 ~ 1 1 1 0 5

# Count red and blue players within 5 blocks
execute store result score #dom_red {ns}.data if entity @a[distance=..5,gamemode=!spectator,scores={{{ns}.mp.in_game=1,{ns}.mp.team=1}}]
execute store result score #dom_blue {ns}.data if entity @a[distance=..5,gamemode=!spectator,scores={{{ns}.mp.in_game=1,{ns}.mp.team=2}}]

# If contested (both teams present), no progress change
execute if score #dom_red {ns}.data matches 1.. if score #dom_blue {ns}.data matches 1.. run return fail

# If only red present: progress toward red (increase toward 100)
execute if score #dom_red {ns}.data matches 1.. unless score #dom_blue {ns}.data matches 1.. run function {ns}:v{version}/multiplayer/gamemodes/dom/capture_red

# If only blue present: progress toward blue (decrease toward -100)
execute if score #dom_blue {ns}.data matches 1.. unless score #dom_red {ns}.data matches 1.. run function {ns}:v{version}/multiplayer/gamemodes/dom/capture_blue
""")

	## DOM: Capture for red/blue (parameterized mirror)
	DOM_LABELS: list[str] = ["A", "B", "C", "D", "E"]
	for color, team_name, owner_id, op, cap, cap_match, neut_old, neut_new, pitch in [
		("red",  "Red",  1, "add",    100,  "101..",  "..-1", "0..",  "1.2"),
		("blue", "Blue", 2, "remove", -100, "..-101", "1..",  "..0",  "0.8"),
	]:
		neutralize_labels: str = "\n".join(
			f'execute if score #dom_prog {ns}.data matches {neut_old} if score @s {ns}.mp.dom_progress matches {neut_new} '
			f'if entity @s[tag={ns}.dom_label_{lbl}] run tellraw @a [{MGS_TAG},{{"text":"Point {lbl} neutralized!","color":"yellow"}}]'
			for lbl in DOM_LABELS
		)
		capture_labels: str = "\n".join(
			f'execute if score @s {ns}.mp.dom_progress matches {cap} unless score @s {ns}.mp.dom_owner matches {owner_id} '
			f'if entity @s[tag={ns}.dom_label_{lbl}] run tellraw @a [{MGS_TAG},{{"text":"{team_name}","color":"{color}"}}," ",{{"text":"captured point {lbl}!","color":"yellow"}}]'
			for lbl in DOM_LABELS
		)
		write_versioned_function(f"multiplayer/gamemodes/dom/capture_{color}", f"""
execute store result score #dom_prog {ns}.data run scoreboard players get @s {ns}.mp.dom_progress
scoreboard players {op} @s {ns}.mp.dom_progress 2

# Cap at {cap}
execute if score @s {ns}.mp.dom_progress matches {cap_match} run scoreboard players set @s {ns}.mp.dom_progress {cap}

# If crossed 0, point neutralized
{neutralize_labels}
execute if score #dom_prog {ns}.data matches {neut_old} if score @s {ns}.mp.dom_progress matches {neut_new} run playsound minecraft:block.note_block.bass player @a ~ ~ ~ 1 0.5
execute if score #dom_prog {ns}.data matches {neut_old} if score @s {ns}.mp.dom_progress matches {neut_new} run scoreboard players set @s {ns}.mp.dom_owner 0
execute if score #dom_prog {ns}.data matches {neut_old} if score @s {ns}.mp.dom_progress matches {neut_new} run data modify entity @n[tag={ns}.dom_label,distance=..1] text.color set value "yellow"

# If reached {cap}, captured by {color}
{capture_labels}
execute if score @s {ns}.mp.dom_progress matches {cap} unless score @s {ns}.mp.dom_owner matches {owner_id} run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 {pitch}
execute if score @s {ns}.mp.dom_progress matches {cap} unless score @s {ns}.mp.dom_owner matches {owner_id} run data modify entity @n[tag={ns}.dom_label,distance=..1] text.color set value "{color}"
execute if score @s {ns}.mp.dom_progress matches {cap} unless score @s {ns}.mp.dom_owner matches {owner_id} run scoreboard players set @s {ns}.mp.dom_owner {owner_id}
""")

	## DOM: Score tick - +1 per owned point
	write_versioned_function("multiplayer/gamemodes/dom/score_tick", f"""
# Count red-owned and blue-owned points
execute store result score #dom_r {ns}.data if entity @e[tag={ns}.dom_point,scores={{{ns}.mp.dom_owner=1}}]
execute store result score #dom_b {ns}.data if entity @e[tag={ns}.dom_point,scores={{{ns}.mp.dom_owner=2}}]

# Add to team scores
scoreboard players operation #red {ns}.mp.team += #dom_r {ns}.data
scoreboard players operation #blue {ns}.mp.team += #dom_b {ns}.data

# Refresh DOM sidebar with updated point ownership
function {ns}:v{version}/multiplayer/refresh_sidebar_dom

# Check win
function {ns}:v{version}/multiplayer/check_team_win
""")

	## DOM: Point particles (colored by owner) - base ring + vertical beam
	write_versioned_function("multiplayer/gamemodes/dom/point_particles", f"""
# Base ring around zone
scoreboard players add @s {ns}.mp.dom_owner 0
execute if score @s {ns}.mp.dom_owner matches 0 run particle dust{{color:[1.0,1.0,1.0],scale:1.5}} ~ ~0.5 ~ 2.5 0.3 2.5 0 10
execute if score @s {ns}.mp.dom_owner matches 1 run particle dust{{color:[1.0,0.2,0.2],scale:1.5}} ~ ~0.5 ~ 2.5 0.3 2.5 0 10
execute if score @s {ns}.mp.dom_owner matches 2 run particle dust{{color:[0.2,0.2,1.0],scale:1.5}} ~ ~0.5 ~ 2.5 0.3 2.5 0 10

# Vertical beam (visible from distance)
execute if score @s {ns}.mp.dom_owner matches 0 run particle dust{{color:[1.0,1.0,1.0],scale:2.0}} ~ ~8 ~ 0.1 2.0 0.1 0 3
execute if score @s {ns}.mp.dom_owner matches 1 run particle dust{{color:[1.0,0.2,0.2],scale:2.0}} ~ ~8 ~ 0.1 2.0 0.1 0 3
execute if score @s {ns}.mp.dom_owner matches 2 run particle dust{{color:[0.2,0.2,1.0],scale:2.0}} ~ ~8 ~ 0.1 2.0 0.1 0 3
""")

	## DOM Kill Hook: Kills also give +1 to team
	write_versioned_function("multiplayer/gamemodes/dom/on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
execute if score @s {ns}.mp.team matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players add #blue {ns}.mp.team 1

# Refresh DOM sidebar to show updated team scores and point ownership
function {ns}:v{version}/multiplayer/refresh_sidebar_dom
""")

	## DOM Cleanup: Kill markers and labels
	write_versioned_function("multiplayer/gamemodes/dom/cleanup", f"""
kill @e[tag={ns}.dom_point]
kill @e[tag={ns}.dom_label]
""")

