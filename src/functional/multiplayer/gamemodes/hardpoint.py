""" Hardpoint: hold a rotating zone to score. """
# Imports
from ...helpers import MGS_TAG
from ...progression import Xp
from .base import GameModeVariant

# Constants
HOLD_XP_SECONDS: int = 5
""" Seconds inside the active hill per 1 XP.
score_tick runs once a second; paying every tick would make sitting on the hill for a ten-minute match worth
more XP than the entire kill feed, so the hold stream is throttled to a fifth of the scoring rate. """


# Classes
class Hardpoint(GameModeVariant):
	""" Hardpoint: a rotating zone; the team that exclusively holds it scores over time. """

	key = "hp"

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		## HP Setup: Initialize zone data from map
		self.sub("setup", f"""
tellraw @a [{MGS_TAG},{{"text":"Hardpoint! Control the zone to score!","color":"yellow"}}]

# Store base coordinates for offset
function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

# Copy hardpoint zones from map to game state
data modify storage {ns}:multiplayer game.hp_zones set from storage {ns}:multiplayer game.map.hardpoint

# Rotation timer (60 seconds = 1200 ticks per zone)
scoreboard players set #hp_rotate_timer {ns}.data 1200

# Rotation timer in seconds for sidebar display
scoreboard players set #hp_rotate_sec {ns}.data 60

# Label index for current hardpoint zone (A, B, C, D, E)
scoreboard players set #hp_zone_idx {ns}.data 0

# Scoring timer (score every 1 second = 20 ticks)
scoreboard players set #hp_score_timer {ns}.data 20

# XP throttles: the hold counter, and the once-per-hill capture flag load_zone clears on every rotation
scoreboard players set #hp_xp_hold {ns}.data {HOLD_XP_SECONDS}

# Load first zone
function {ns}:v{version}/multiplayer/gamemodes/hp/load_zone
""")

		## HP: Load zone from first entry → summon single marker with base offset
		self.sub("load_zone", f"""
# A fresh hill is uncaptured, so the next side to hold it uncontested earns the capture bonus
scoreboard players set #hp_xp_captured {ns}.data 0

# Kill old zone marker
kill @e[tag={ns}.hp_marker]
kill @e[tag={ns}.hp_label]

# Zone point: relative → absolute
execute store result score #rx {ns}.data run data get storage {ns}:multiplayer game.hp_zones[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:multiplayer game.hp_zones[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:multiplayer game.hp_zones[0][2]
scoreboard players operation #rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _hp_pos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _hp_pos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _hp_pos.z double 1 run scoreboard players get #rz {ns}.data

# Assign point label (fallback to HP for maps with >5 zones)
data modify storage {ns}:temp _hp_pos.label set value "HP"
execute if score #hp_zone_idx {ns}.data matches 0 run data modify storage {ns}:temp _hp_pos.label set value "A"
execute if score #hp_zone_idx {ns}.data matches 1 run data modify storage {ns}:temp _hp_pos.label set value "B"
execute if score #hp_zone_idx {ns}.data matches 2 run data modify storage {ns}:temp _hp_pos.label set value "C"
execute if score #hp_zone_idx {ns}.data matches 3 run data modify storage {ns}:temp _hp_pos.label set value "D"
execute if score #hp_zone_idx {ns}.data matches 4 run data modify storage {ns}:temp _hp_pos.label set value "E"
scoreboard players add #hp_zone_idx {ns}.data 1

function {ns}:v{version}/multiplayer/gamemodes/hp/summon_marker with storage {ns}:temp _hp_pos

tellraw @a [{MGS_TAG},"⚡ ",{{"text":"Hardpoint ","color":"dark_purple"}},{{"storage":"{ns}:temp","nbt":"_hp_pos.label","color":"yellow","interpret":true}},{{"text":" active!","color":"dark_purple"}}]
playsound minecraft:block.note_block.chime player @a ~ ~ ~ 1 1.0
""")

		## HP: Summon zone marker (macro)
		self.sub("summon_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.hp_marker","{ns}.gm_entity"]}}
$summon minecraft:text_display $(x) $(y) $(z) {{Tags:["{ns}.hp_label","{ns}.gm_entity","{ns}.hp_$(label)"],billboard:"vertical",text:{{"text":"$(label)","color":"dark_purple","bold":true}},transformation:{{translation:[0.0f,2.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[3.0f,3.0f,3.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}
""")  # noqa: E501

		## HP Tick: Zone particles, scoring, rotation
		self.sub("tick", f"""
# Rotation timer
scoreboard players operation #hp_rotate_timer {ns}.data -= #tick_delta {ns}.data
execute if score #hp_rotate_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/hp/rotate

# Update seconds display for sidebar (ticks / 20)
scoreboard players operation #hp_rotate_sec {ns}.data = #hp_rotate_timer {ns}.data
scoreboard players operation #hp_rotate_sec {ns}.data /= #20 {ns}.data

# Refresh sidebar every second (when score_timer resets)
execute if score #hp_score_timer {ns}.data matches ..1 run function #bs.sidebar:refresh {{objective:"{ns}.sidebar"}}

# Show particles at zone center
execute at @e[tag={ns}.hp_marker] run particle dust{{color:[0.5,0.0,0.5],scale:1.5}} ~ ~ ~ 4 0.5 4 0 10

# Tag players inside the zone (5x5 blocks horizontally, 4 blocks vertically, centered on the marker)
tag @a remove {ns}.in_hp_zone
execute at @e[tag={ns}.hp_marker] positioned ~-2.5 ~-1 ~-2.5 run tag @a[dx=4,dy=3,dz=4,gamemode=!spectator,scores={{{ns}.mp.in_game=1}}] add {ns}.in_hp_zone

# Count teams in zone
execute store result score #hp_red {ns}.data if entity @a[tag={ns}.in_hp_zone,scores={{{ns}.mp.team=1}}]
execute store result score #hp_blue {ns}.data if entity @a[tag={ns}.in_hp_zone,scores={{{ns}.mp.team=2}}]

# Scoring interval
scoreboard players remove #hp_score_timer {ns}.data 1
execute if score #hp_score_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/hp/score_tick
execute if score #hp_score_timer {ns}.data matches ..0 run scoreboard players set #hp_score_timer {ns}.data 20
""")

		## HP: Score tick.
		## Two XP streams here. The capture bonus is a one-off per hill, gated on #hp_xp_captured, which
		## hp/load_zone clears — so it pays whichever side gets there first after a rotation. The hold
		## stream is deliberately 1 XP per HOLD_XP_SECONDS rather than per second: this function runs once a
		## second, and paying every one of them would make camping the hill worth more than the entire kill
		## feed over a ten-minute match.
		alone: dict[int, str] = {
			1: f"if score #hp_red {ns}.data matches 1.. unless score #hp_blue {ns}.data matches 1..",
			2: f"if score #hp_blue {ns}.data matches 1.. unless score #hp_red {ns}.data matches 1..",
		}
		holders: str = f"@a[tag={ns}.in_hp_zone,scores={{{ns}.mp.team=%d,{ns}.mp.in_game=1}}]"
		uncaptured: str = f"if score #hp_xp_captured {ns}.data matches 0"
		due: str = f"if score #hp_xp_hold {ns}.data matches ..0"
		capture_lines: str = "\n".join(
			f'execute {alone[team]} {uncaptured} run tellraw {who} '
			f'[{MGS_TAG},"🎯 ",{{"text":"Hardpoint captured!","color":"gold"}}{suffix}]'
			for team in alone
			for who, suffix in (
				(f"@a[tag=!{ns}.in_hp_zone]", ""),
				(holders % team, "," + Xp.suffix("mp", "hp_capture")),
			)
		) + "\n" + "\n".join(
			Xp.give("mp", "hp_capture", holders % team, guard=f"{alone[team]} {uncaptured}") for team in alone
		)
		hold_lines: str = "\n".join(
			Xp.give("mp", "hp_hold", holders % team, guard=f"{alone[team]} {due}") for team in alone
		)
		self.sub("score_tick", f"""
# Only score if one team exclusively holds the zone (not contested)
# Red alone in zone
execute {alone[1]} at @e[tag={ns}.hp_marker] run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute {alone[1]} run scoreboard players add #red {ns}.mp.team 1

# Blue alone in zone
execute {alone[2]} at @e[tag={ns}.hp_marker] run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute {alone[2]} run scoreboard players add #blue {ns}.mp.team 1

# First side to hold this hill after it rotated
{capture_lines}
execute {alone[1]} run scoreboard players set #hp_xp_captured {ns}.data 1
execute {alone[2]} run scoreboard players set #hp_xp_captured {ns}.data 1

# Holding it, once every {HOLD_XP_SECONDS}s. No message: the bar moving is the feedback.
scoreboard players remove #hp_xp_hold {ns}.data 1
{hold_lines}
execute if score #hp_xp_hold {ns}.data matches ..0 run scoreboard players set #hp_xp_hold {ns}.data {HOLD_XP_SECONDS}

# Check win
function {ns}:v{version}/multiplayer/check_team_win
""")

		## HP: Rotate zone
		self.sub("rotate", f"""
# Remove the first entry (current zone) from the zones list
data remove storage {ns}:multiplayer game.hp_zones[0]

# Check if there are more zones
execute unless data storage {ns}:multiplayer game.hp_zones[0] run function {ns}:v{version}/multiplayer/gamemodes/hp/reset_zones

# Reset rotation timer
scoreboard players set #hp_rotate_timer {ns}.data 1200
scoreboard players set #hp_rotate_sec {ns}.data 60

# Load next zone
function {ns}:v{version}/multiplayer/gamemodes/hp/load_zone
""")

		## HP: Reset zones (cycle back to beginning)
		self.sub("reset_zones", f"""
# Refill zones from map data
data modify storage {ns}:multiplayer game.hp_zones set from storage {ns}:multiplayer game.map.hardpoint
scoreboard players set #hp_zone_idx {ns}.data 0
""")

		## HP Kill Hook: Same as TDM (+1 team)
		self.sub("on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
execute if score @s {ns}.mp.team matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players add #blue {ns}.mp.team 1

# Refresh sidebar to show updated team scores
function #bs.sidebar:refresh {{objective:"{ns}.sidebar"}}
""")

		## HP Cleanup
		self.sub("cleanup", f"""
kill @e[tag={ns}.hp_marker]
kill @e[tag={ns}.hp_label]
tag @a remove {ns}.in_hp_zone
""")

# Functions
def generate_hardpoint() -> None:
	""" Module-level entry point (preserved signature); delegates to :class:`Hardpoint`. """
	Hardpoint()()

