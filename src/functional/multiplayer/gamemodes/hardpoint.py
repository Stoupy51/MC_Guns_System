
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG


def generate_hardpoint() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## HP Setup: Initialize zone data from map
	write_versioned_function("multiplayer/gamemodes/hp/setup", f"""
tellraw @a [{MGS_TAG},{{"text":"Hardpoint! Control the zone to score!","color":"yellow"}}]

# Store base coordinates for offset
execute store result score #gm_base_x {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[0]
execute store result score #gm_base_y {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[1]
execute store result score #gm_base_z {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[2]

# Copy hardpoint zones from map to game state
data modify storage {ns}:multiplayer game.hp_zones set from storage {ns}:multiplayer game.map.hardpoint

# Rotation timer (60 seconds = 1200 ticks per zone)
scoreboard players set #hp_rotate_timer {ns}.data 1200

# Scoring timer (score every 1 second = 20 ticks)
scoreboard players set #hp_score_timer {ns}.data 20

# Load first zone
function {ns}:v{version}/multiplayer/gamemodes/hp/load_zone
""")

	## HP: Load zone from first 2 entries → summon corner markers with base offset
	write_versioned_function("multiplayer/gamemodes/hp/load_zone", f"""
# Kill old zone markers
kill @e[tag={ns}.hp_corner]

# Corner A: relative → absolute
execute store result score #_rx {ns}.data run data get storage {ns}:multiplayer game.hp_zones[0][0]
execute store result score #_ry {ns}.data run data get storage {ns}:multiplayer game.hp_zones[0][1]
execute store result score #_rz {ns}.data run data get storage {ns}:multiplayer game.hp_zones[0][2]
scoreboard players operation #_rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _hp_pos.x double 1 run scoreboard players get #_rx {ns}.data
execute store result storage {ns}:temp _hp_pos.y double 1 run scoreboard players get #_ry {ns}.data
execute store result storage {ns}:temp _hp_pos.z double 1 run scoreboard players get #_rz {ns}.data
function {ns}:v{version}/multiplayer/gamemodes/hp/summon_corner_a with storage {ns}:temp _hp_pos

# Corner B: relative → absolute
execute if data storage {ns}:multiplayer game.hp_zones[1] store result score #_rx {ns}.data run data get storage {ns}:multiplayer game.hp_zones[1][0]
execute if data storage {ns}:multiplayer game.hp_zones[1] store result score #_ry {ns}.data run data get storage {ns}:multiplayer game.hp_zones[1][1]
execute if data storage {ns}:multiplayer game.hp_zones[1] store result score #_rz {ns}.data run data get storage {ns}:multiplayer game.hp_zones[1][2]
scoreboard players operation #_rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _hp_pos.x double 1 run scoreboard players get #_rx {ns}.data
execute store result storage {ns}:temp _hp_pos.y double 1 run scoreboard players get #_ry {ns}.data
execute store result storage {ns}:temp _hp_pos.z double 1 run scoreboard players get #_rz {ns}.data
execute if data storage {ns}:multiplayer game.hp_zones[1] run function {ns}:v{version}/multiplayer/gamemodes/hp/summon_corner_b with storage {ns}:temp _hp_pos

tellraw @a [{MGS_TAG},{{"text":"⚡ Hardpoint zone active!","color":"dark_purple"}}]
playsound minecraft:block.note_block.chime player @a ~ ~ ~ 1 1.0
""")

	## HP: Summon corner markers (macros)
	write_versioned_function("multiplayer/gamemodes/hp/summon_corner_a", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.hp_corner","{ns}.hp_corner_a","{ns}.gm_entity"]}}
""")
	write_versioned_function("multiplayer/gamemodes/hp/summon_corner_b", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.hp_corner","{ns}.hp_corner_b","{ns}.gm_entity"]}}
""")

	## HP Tick: Zone particles, scoring, rotation
	write_versioned_function("multiplayer/gamemodes/hp/tick", f"""
# Rotation timer
scoreboard players remove #hp_rotate_timer {ns}.data 1
execute if score #hp_rotate_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/hp/rotate

# Show particles at zone corners
execute at @e[tag={ns}.hp_corner] run particle dust{{color:[0.5,0.0,0.5],scale:1.5}} ~ ~1 ~ 4 0.5 4 0 10

# Count teams in zone: check players between the two corners
# Store corner A position
execute as @e[tag={ns}.hp_corner_a] store result score #hp_ax {ns}.data run data get entity @s Pos[0]
execute as @e[tag={ns}.hp_corner_a] store result score #hp_ay {ns}.data run data get entity @s Pos[1]
execute as @e[tag={ns}.hp_corner_a] store result score #hp_az {ns}.data run data get entity @s Pos[2]
# Store corner B position
execute as @e[tag={ns}.hp_corner_b] store result score #hp_bx {ns}.data run data get entity @s Pos[0]
execute as @e[tag={ns}.hp_corner_b] store result score #hp_by {ns}.data run data get entity @s Pos[1]
execute as @e[tag={ns}.hp_corner_b] store result score #hp_bz {ns}.data run data get entity @s Pos[2]

# Tag players inside the zone (between both corners with 3-block margin)
# Using positioned checking: player must be within 8 blocks of BOTH corners
# TODO: optimize this shit
tag @a remove {ns}.in_hp_zone
execute at @e[tag={ns}.hp_corner_a] as @a[distance=..15] at @s at @e[tag={ns}.hp_corner_b,distance=..15] run tag @s add {ns}.in_hp_zone

# Count teams in zone
execute store result score #hp_red {ns}.data if entity @a[tag={ns}.in_hp_zone,scores={{{ns}.mp.team=1}}]
execute store result score #hp_blue {ns}.data if entity @a[tag={ns}.in_hp_zone,scores={{{ns}.mp.team=2}}]

# Scoring interval
scoreboard players remove #hp_score_timer {ns}.data 1
execute if score #hp_score_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/hp/score_tick
execute if score #hp_score_timer {ns}.data matches ..0 run scoreboard players set #hp_score_timer {ns}.data 20
""")

	## HP: Score tick
	write_versioned_function("multiplayer/gamemodes/hp/score_tick", f"""
# Only score if one team exclusively holds the zone (not contested)
# Red alone in zone
execute if score #hp_red {ns}.data matches 1.. unless score #hp_blue {ns}.data matches 1.. at @e[tag={ns}.hp_corner] run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute if score #hp_red {ns}.data matches 1.. unless score #hp_blue {ns}.data matches 1.. run scoreboard players add #red {ns}.mp.team 1

# Blue alone in zone
execute if score #hp_blue {ns}.data matches 1.. unless score #hp_red {ns}.data matches 1.. at @e[tag={ns}.hp_corner] run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute if score #hp_blue {ns}.data matches 1.. unless score #hp_red {ns}.data matches 1.. run scoreboard players add #blue {ns}.mp.team 1

# Check win
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score #red {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
""")

	## HP: Rotate zone
	write_versioned_function("multiplayer/gamemodes/hp/rotate", f"""
# Remove the first 2 entries (current zone pair) from the zones list
data remove storage {ns}:multiplayer game.hp_zones[0]
data remove storage {ns}:multiplayer game.hp_zones[0]

# Check if there are more zones
execute unless data storage {ns}:multiplayer game.hp_zones[0] run function {ns}:v{version}/multiplayer/gamemodes/hp/reset_zones

# Reset rotation timer
scoreboard players set #hp_rotate_timer {ns}.data 1200

# Load next zone
function {ns}:v{version}/multiplayer/gamemodes/hp/load_zone
""")

	## HP: Reset zones (cycle back to beginning)
	write_versioned_function("multiplayer/gamemodes/hp/reset_zones", f"""
# Refill zones from map data
data modify storage {ns}:multiplayer game.hp_zones set from storage {ns}:multiplayer game.map.hardpoint
scoreboard players set #hp_zone_idx {ns}.data 0
""")

	## HP Kill Hook: Same as TDM (+1 team)
	write_versioned_function("multiplayer/gamemodes/hp/on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
execute if score @s {ns}.mp.team matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players add #blue {ns}.mp.team 1
""")

	## HP Cleanup
	write_versioned_function("multiplayer/gamemodes/hp/cleanup", f"""
kill @e[tag={ns}.hp_corner]
tag @a remove {ns}.in_hp_zone
""")
