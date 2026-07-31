""" Domination: capture and hold three points for score over time. """
# ruff: noqa: E501
# Imports
from ...helpers import MGS_TAG
from ...progression import Xp
from .base import GameModeVariant


# Classes
class Domination(GameModeVariant):
	""" Domination: capture and hold lettered zones (A-E) to earn points over time. """

	key = "dom"

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		## DOM Setup: Summon capture point markers from loaded map
		self.sub("setup", f"""
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
		self.sub("summon_point", f"""
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
		self.sub("summon_point_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.dom_point","{ns}.gm_entity","{ns}.dom_label_$(label)"]}}
$summon minecraft:text_display $(x) $(y) $(z) {{Tags:["{ns}.dom_label","{ns}.gm_entity","{ns}.dom_$(label)"],billboard:"vertical",text:{{"text":"$(label)","color":"yellow","bold":true}},transformation:{{translation:[0.0f,2.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[3.0f,3.0f,3.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}
""")

		## DOM Tick: Check capture progress + score
		self.sub("tick", f"""
# Process each domination point
execute as @e[tag={ns}.dom_point] at @s run function {ns}:v{version}/multiplayer/gamemodes/dom/point_tick

# Sync point ownership to global scores for sidebar display
execute as @e[tag={ns}.dom_point,tag={ns}.dom_label_A] store result score #dom_owner_a {ns}.data run scoreboard players get @s {ns}.mp.dom_owner
execute as @e[tag={ns}.dom_point,tag={ns}.dom_label_B] store result score #dom_owner_b {ns}.data run scoreboard players get @s {ns}.mp.dom_owner
execute as @e[tag={ns}.dom_point,tag={ns}.dom_label_C] store result score #dom_owner_c {ns}.data run scoreboard players get @s {ns}.mp.dom_owner
execute as @e[tag={ns}.dom_point,tag={ns}.dom_label_D] store result score #dom_owner_d {ns}.data run scoreboard players get @s {ns}.mp.dom_owner
execute as @e[tag={ns}.dom_point,tag={ns}.dom_label_E] store result score #dom_owner_e {ns}.data run scoreboard players get @s {ns}.mp.dom_owner

# Scoring interval
scoreboard players operation #dom_score_timer {ns}.data -= #tick_delta {ns}.data
execute if score #dom_score_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/dom/score_tick
execute if score #dom_score_timer {ns}.data matches ..0 run scoreboard players set #dom_score_timer {ns}.data 100

# Show particles at each point
execute as @e[tag={ns}.dom_point] at @s run function {ns}:v{version}/multiplayer/gamemodes/dom/point_particles
""")

		## DOM: Per-point tick - check nearby players and adjust capture
		self.sub("point_tick", f"""
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
			## Both announces are emitted twice: once to the players standing on the point, carrying the XP
			## they just earned, and once to everyone else without it. A tellraw is one atomic message and a
			## score component resolves in the executor's context, not per recipient, so a single line
			## cannot say "+20 XP" to only some of the people reading it.
			CAPTURER: str = f"{ns}.dom_capturer"
			neut_guard: str = (
				f'execute if score #dom_prog {ns}.data matches {neut_old} '
				f'if score @s {ns}.mp.dom_progress matches {neut_new}'
			)
			cap_guard: str = (
				f'execute if score @s {ns}.mp.dom_progress matches {cap} '
				f'unless score @s {ns}.mp.dom_owner matches {owner_id}'
			)
			neutralize_labels: str = "\n".join(
				f'{neut_guard} if entity @s[tag={ns}.dom_label_{lbl}] run tellraw {who} '
				f'[{MGS_TAG},{{"text":"Point {lbl} neutralized!","color":"yellow"}}{suffix}]'
				for lbl in DOM_LABELS
				for who, suffix in (
					(f"@a[tag=!{CAPTURER}]", ""),
					(f"@a[tag={CAPTURER}]", "," + Xp.suffix("mp", "dom_neutralize")),
				)
			)
			capture_labels: str = "\n".join(
				f'{cap_guard} if entity @s[tag={ns}.dom_label_{lbl}] run tellraw {who} '
				f'[{MGS_TAG},{{"text":"{team_name}","color":"{color}"}}," ",{{"text":"captured point {lbl}!","color":"yellow"}}{suffix}]'
				for lbl in DOM_LABELS
				for who, suffix in (
					(f"@a[tag=!{CAPTURER}]", ""),
					(f"@a[tag={CAPTURER}]", "," + Xp.suffix("mp", "dom_capture")),
				)
			)
			## @s = the point marker, at it, so the players who did the work are whoever is inside its radius
			## on the tick it flips. Awarded and announced BEFORE dom_owner moves: the guard above reads it,
			## so anything placed after that `set` would never fire.
			nearby: str = f"@a[distance=..5,scores={{{ns}.mp.team={owner_id},{ns}.mp.in_game=1}}]"
			self.sub(f"capture_{color}", f"""
execute store result score #dom_prog {ns}.data run scoreboard players get @s {ns}.mp.dom_progress
scoreboard players {op} @s {ns}.mp.dom_progress 2

# Cap at {cap}
execute if score @s {ns}.mp.dom_progress matches {cap_match} run scoreboard players set @s {ns}.mp.dom_progress {cap}

# If crossed 0, point neutralized
tag @a remove {CAPTURER}
{neut_guard} run tag {nearby} add {CAPTURER}
{neutralize_labels}
{Xp.give("mp", "dom_neutralize", f"@a[tag={CAPTURER}]")}
{neut_guard} run playsound minecraft:block.note_block.bass player @a ~ ~ ~ 1 0.5
{neut_guard} run scoreboard players set @s {ns}.mp.dom_owner 0
{neut_guard} run data modify entity @n[tag={ns}.dom_label,distance=..1] text.color set value "yellow"

# If reached {cap}, captured by {color}
tag @a remove {CAPTURER}
{cap_guard} run tag {nearby} add {CAPTURER}
{capture_labels}
{Xp.give("mp", "dom_capture", f"@a[tag={CAPTURER}]")}
{cap_guard} run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 {pitch}
{cap_guard} run data modify entity @n[tag={ns}.dom_label,distance=..1] text.color set value "{color}"
{cap_guard} run scoreboard players set @s {ns}.mp.dom_owner {owner_id}
tag @a remove {CAPTURER}
""")

		## DOM: Score tick - +1 per owned point
		self.sub("score_tick", f"""
# Count red-owned and blue-owned points
execute store result score #dom_r {ns}.data if entity @e[tag={ns}.dom_point,scores={{{ns}.mp.dom_owner=1}}]
execute store result score #dom_b {ns}.data if entity @e[tag={ns}.dom_point,scores={{{ns}.mp.dom_owner=2}}]

# Add to team scores
scoreboard players operation #red {ns}.mp.team += #dom_r {ns}.data
scoreboard players operation #blue {ns}.mp.team += #dom_b {ns}.data

# XP for actually standing on a point your team holds, rather than for the team owning it from anywhere.
# This tick is already the 5s cadence, so it is one award per point held per 5s. Before check_team_win:
# that can end the match, and the cleanup it runs would leave nobody left to pay.
execute as @e[tag={ns}.dom_point,scores={{{ns}.mp.dom_owner=1}}] at @s run {Xp.give("mp", "dom_hold", f"@a[distance=..5,scores={{{ns}.mp.team=1,{ns}.mp.in_game=1}}]")}
execute as @e[tag={ns}.dom_point,scores={{{ns}.mp.dom_owner=2}}] at @s run {Xp.give("mp", "dom_hold", f"@a[distance=..5,scores={{{ns}.mp.team=2,{ns}.mp.in_game=1}}]")}

# Refresh DOM sidebar with updated point ownership
function {ns}:v{version}/multiplayer/refresh_sidebar_dom

# Check win
function {ns}:v{version}/multiplayer/check_team_win
""")

		## DOM: Point particles (colored by owner) - base ring + vertical beam
		self.sub("point_particles", f"""
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
		self.sub("on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
execute if score @s {ns}.mp.team matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players add #blue {ns}.mp.team 1

# Refresh DOM sidebar to show updated team scores and point ownership
function {ns}:v{version}/multiplayer/refresh_sidebar_dom
""")

		## DOM Cleanup: Kill markers and labels
		self.sub("cleanup", f"""
kill @e[tag={ns}.dom_point]
kill @e[tag={ns}.dom_label]
""")

# Functions
def generate_domination() -> None:
	""" Module-level entry point (preserved signature); delegates to :class:`Domination`. """
	Domination()()

