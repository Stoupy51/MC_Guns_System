
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

	## DOM: Capture for red (progress goes +)
	write_versioned_function("multiplayer/gamemodes/dom/capture_red", f"""
# Get current progress
execute store result score #dom_prog {ns}.data run scoreboard players get @s {ns}.mp.dom_progress

# Increase progress (2 per tick when capturing)
scoreboard players add @s {ns}.mp.dom_progress 2

# Cap at 100
execute if score @s {ns}.mp.dom_progress matches 101.. run scoreboard players set @s {ns}.mp.dom_progress 100

# If crossed 0 from negative (was blue, now contested), briefly neutral
execute if score #dom_prog {ns}.data matches ..-1 if score @s {ns}.mp.dom_progress matches 0.. if entity @s[tag={ns}.dom_label_A] run tellraw @a [{MGS_TAG},{{"text":"Point A neutralized!","color":"yellow"}}]
execute if score #dom_prog {ns}.data matches ..-1 if score @s {ns}.mp.dom_progress matches 0.. if entity @s[tag={ns}.dom_label_B] run tellraw @a [{MGS_TAG},{{"text":"Point B neutralized!","color":"yellow"}}]
execute if score #dom_prog {ns}.data matches ..-1 if score @s {ns}.mp.dom_progress matches 0.. if entity @s[tag={ns}.dom_label_C] run tellraw @a [{MGS_TAG},{{"text":"Point C neutralized!","color":"yellow"}}]
execute if score #dom_prog {ns}.data matches ..-1 if score @s {ns}.mp.dom_progress matches 0.. if entity @s[tag={ns}.dom_label_D] run tellraw @a [{MGS_TAG},{{"text":"Point D neutralized!","color":"yellow"}}]
execute if score #dom_prog {ns}.data matches ..-1 if score @s {ns}.mp.dom_progress matches 0.. if entity @s[tag={ns}.dom_label_E] run tellraw @a [{MGS_TAG},{{"text":"Point E neutralized!","color":"yellow"}}]
execute if score #dom_prog {ns}.data matches ..-1 if score @s {ns}.mp.dom_progress matches 0.. run playsound minecraft:block.note_block.bass player @a ~ ~ ~ 1 0.5
execute if score #dom_prog {ns}.data matches ..-1 if score @s {ns}.mp.dom_progress matches 0.. run scoreboard players set @s {ns}.mp.dom_owner 0
execute if score #dom_prog {ns}.data matches ..-1 if score @s {ns}.mp.dom_progress matches 0.. run data modify entity @n[tag={ns}.dom_label,distance=..1] text.color set value "yellow"

# If reached 100, captured by red
execute if score @s {ns}.mp.dom_progress matches 100 unless score @s {ns}.mp.dom_owner matches 1 if entity @s[tag={ns}.dom_label_A] run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}}," ",{{"text":"captured point A!","color":"yellow"}}]
execute if score @s {ns}.mp.dom_progress matches 100 unless score @s {ns}.mp.dom_owner matches 1 if entity @s[tag={ns}.dom_label_B] run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}}," ",{{"text":"captured point B!","color":"yellow"}}]
execute if score @s {ns}.mp.dom_progress matches 100 unless score @s {ns}.mp.dom_owner matches 1 if entity @s[tag={ns}.dom_label_C] run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}}," ",{{"text":"captured point C!","color":"yellow"}}]
execute if score @s {ns}.mp.dom_progress matches 100 unless score @s {ns}.mp.dom_owner matches 1 if entity @s[tag={ns}.dom_label_D] run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}}," ",{{"text":"captured point D!","color":"yellow"}}]
execute if score @s {ns}.mp.dom_progress matches 100 unless score @s {ns}.mp.dom_owner matches 1 if entity @s[tag={ns}.dom_label_E] run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}}," ",{{"text":"captured point E!","color":"yellow"}}]
execute if score @s {ns}.mp.dom_progress matches 100 unless score @s {ns}.mp.dom_owner matches 1 run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute if score @s {ns}.mp.dom_progress matches 100 unless score @s {ns}.mp.dom_owner matches 1 run data modify entity @n[tag={ns}.dom_label,distance=..1] text.color set value "red"
execute if score @s {ns}.mp.dom_progress matches 100 unless score @s {ns}.mp.dom_owner matches 1 run scoreboard players set @s {ns}.mp.dom_owner 1
""")

	## DOM: Capture for blue (progress goes -)
	write_versioned_function("multiplayer/gamemodes/dom/capture_blue", f"""
# Decrease progress (2 per tick when capturing)
execute store result score #dom_prog {ns}.data run scoreboard players get @s {ns}.mp.dom_progress
scoreboard players remove @s {ns}.mp.dom_progress 2

# Cap at -100
execute if score @s {ns}.mp.dom_progress matches ..-101 run scoreboard players set @s {ns}.mp.dom_progress -100

# If crossed 0 from positive (was red, now contested)
execute if score #dom_prog {ns}.data matches 1.. if score @s {ns}.mp.dom_progress matches ..0 if entity @s[tag={ns}.dom_label_A] run tellraw @a [{MGS_TAG},{{"text":"Point A neutralized!","color":"yellow"}}]
execute if score #dom_prog {ns}.data matches 1.. if score @s {ns}.mp.dom_progress matches ..0 if entity @s[tag={ns}.dom_label_B] run tellraw @a [{MGS_TAG},{{"text":"Point B neutralized!","color":"yellow"}}]
execute if score #dom_prog {ns}.data matches 1.. if score @s {ns}.mp.dom_progress matches ..0 if entity @s[tag={ns}.dom_label_C] run tellraw @a [{MGS_TAG},{{"text":"Point C neutralized!","color":"yellow"}}]
execute if score #dom_prog {ns}.data matches 1.. if score @s {ns}.mp.dom_progress matches ..0 if entity @s[tag={ns}.dom_label_D] run tellraw @a [{MGS_TAG},{{"text":"Point D neutralized!","color":"yellow"}}]
execute if score #dom_prog {ns}.data matches 1.. if score @s {ns}.mp.dom_progress matches ..0 if entity @s[tag={ns}.dom_label_E] run tellraw @a [{MGS_TAG},{{"text":"Point E neutralized!","color":"yellow"}}]
execute if score #dom_prog {ns}.data matches 1.. if score @s {ns}.mp.dom_progress matches ..0 run playsound minecraft:block.note_block.bass player @a ~ ~ ~ 1 0.5
execute if score #dom_prog {ns}.data matches 1.. if score @s {ns}.mp.dom_progress matches ..0 run scoreboard players set @s {ns}.mp.dom_owner 0
execute if score #dom_prog {ns}.data matches 1.. if score @s {ns}.mp.dom_progress matches ..0 run data modify entity @n[tag={ns}.dom_label,distance=..1] text.color set value "yellow"

# If reached -100, captured by blue
execute if score @s {ns}.mp.dom_progress matches -100 unless score @s {ns}.mp.dom_owner matches 2 if entity @s[tag={ns}.dom_label_A] run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}}," ",{{"text":"captured point A!","color":"yellow"}}]
execute if score @s {ns}.mp.dom_progress matches -100 unless score @s {ns}.mp.dom_owner matches 2 if entity @s[tag={ns}.dom_label_B] run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}}," ",{{"text":"captured point B!","color":"yellow"}}]
execute if score @s {ns}.mp.dom_progress matches -100 unless score @s {ns}.mp.dom_owner matches 2 if entity @s[tag={ns}.dom_label_C] run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}}," ",{{"text":"captured point C!","color":"yellow"}}]
execute if score @s {ns}.mp.dom_progress matches -100 unless score @s {ns}.mp.dom_owner matches 2 if entity @s[tag={ns}.dom_label_D] run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}}," ",{{"text":"captured point D!","color":"yellow"}}]
execute if score @s {ns}.mp.dom_progress matches -100 unless score @s {ns}.mp.dom_owner matches 2 if entity @s[tag={ns}.dom_label_E] run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}}," ",{{"text":"captured point E!","color":"yellow"}}]
execute if score @s {ns}.mp.dom_progress matches -100 unless score @s {ns}.mp.dom_owner matches 2 run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 0.8
execute if score @s {ns}.mp.dom_progress matches -100 unless score @s {ns}.mp.dom_owner matches 2 run data modify entity @n[tag={ns}.dom_label,distance=..1] text.color set value "blue"
execute if score @s {ns}.mp.dom_progress matches -100 unless score @s {ns}.mp.dom_owner matches 2 run scoreboard players set @s {ns}.mp.dom_owner 2
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
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score #red {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
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

