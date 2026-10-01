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

		self.sub("setup", f"""
tellraw @a [{MGS_TAG},{{"text":"Hardpoint! Control the zone to score!","color":"yellow"}}]

function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

data modify storage {ns}:multiplayer game.hp_zones set from storage {ns}:multiplayer game.map.hardpoint

# 60 s per zone.
scoreboard players set #hp_rotate_timer {ns}.data 1200

# For the sidebar.
scoreboard players set #hp_rotate_sec {ns}.data 60

# Label of the current zone (A to E).
scoreboard players set #hp_zone_idx {ns}.data 0

# Score every second.
scoreboard players set #hp_score_timer {ns}.data 20

# XP throttles: the hold counter, and the once-per-hill capture flag that load_zone clears.
scoreboard players set #hp_xp_hold {ns}.data {HOLD_XP_SECONDS}

function {ns}:v{version}/multiplayer/gamemodes/hp/load_zone
""")

		## Summons the first zone in the list, offset from the base.
		self.sub("load_zone", f"""
# A fresh hill is uncaptured: the next side to hold it alone earns the capture bonus.
scoreboard players set #hp_xp_captured {ns}.data 0

kill @e[tag={ns}.hp_marker]
kill @e[tag={ns}.hp_label]

execute store result score #rx {ns}.data run data get storage {ns}:multiplayer game.hp_zones[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:multiplayer game.hp_zones[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:multiplayer game.hp_zones[0][2]
scoreboard players operation #rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _hp_pos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _hp_pos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _hp_pos.z double 1 run scoreboard players get #rz {ns}.data

# "HP" for maps with more than 5 zones.
data modify storage {ns}:temp _hp_pos.label set value "HP"
execute if score #hp_zone_idx {ns}.data matches 0 run data modify storage {ns}:temp _hp_pos.label set value "A"
execute if score #hp_zone_idx {ns}.data matches 1 run data modify storage {ns}:temp _hp_pos.label set value "B"
execute if score #hp_zone_idx {ns}.data matches 2 run data modify storage {ns}:temp _hp_pos.label set value "C"
execute if score #hp_zone_idx {ns}.data matches 3 run data modify storage {ns}:temp _hp_pos.label set value "D"
execute if score #hp_zone_idx {ns}.data matches 4 run data modify storage {ns}:temp _hp_pos.label set value "E"
scoreboard players add #hp_zone_idx {ns}.data 1

function {ns}:v{version}/multiplayer/gamemodes/hp/summon_marker with storage {ns}:temp _hp_pos

tellraw @a [{MGS_TAG},{{"text":"⚡ ","color":"white"}},{{"text":"Hardpoint ","color":"dark_purple"}},{{"storage":"{ns}:temp","nbt":"_hp_pos.label","color":"yellow","interpret":true}},{{"text":" active!","color":"dark_purple"}}]
playsound minecraft:block.note_block.chime player @a ~ ~ ~ 1 1.0
""")

		self.sub("summon_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.hp_marker","{ns}.gm_entity"]}}
$summon minecraft:text_display $(x) $(y) $(z) {{Tags:["{ns}.hp_label","{ns}.gm_entity","{ns}.hp_$(label)"],billboard:"vertical",text:{{"text":"$(label)","color":"dark_purple","bold":true}},transformation:{{translation:[0.0f,2.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[3.0f,3.0f,3.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}
""")

		self.sub("tick", f"""
scoreboard players operation #hp_rotate_timer {ns}.data -= #tick_delta {ns}.data
execute if score #hp_rotate_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/hp/rotate

scoreboard players operation #hp_rotate_sec {ns}.data = #hp_rotate_timer {ns}.data
scoreboard players operation #hp_rotate_sec {ns}.data /= #20 {ns}.data

# Every second.
execute if score #hp_score_timer {ns}.data matches ..1 run function #bs.sidebar:refresh {{objective:"{ns}.sidebar"}}

execute at @e[tag={ns}.hp_marker] run particle dust{{color:[0.5,0.0,0.5],scale:1.5}} ~ ~ ~ 4 0.5 4 0 10

# 5x5 horizontally, 4 vertically, centred on the marker.
tag @a remove {ns}.in_hp_zone
execute at @e[tag={ns}.hp_marker] positioned ~-2.5 ~-1 ~-2.5 run tag @a[dx=4,dy=3,dz=4,gamemode=!spectator,scores={{{ns}.mp.in_game=1}}] add {ns}.in_hp_zone

execute store result score #hp_red {ns}.data if entity @a[tag={ns}.in_hp_zone,scores={{{ns}.mp.team=1}}]
execute store result score #hp_blue {ns}.data if entity @a[tag={ns}.in_hp_zone,scores={{{ns}.mp.team=2}}]

scoreboard players remove #hp_score_timer {ns}.data 1
execute if score #hp_score_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/hp/score_tick
execute if score #hp_score_timer {ns}.data matches ..0 run scoreboard players set #hp_score_timer {ns}.data 20
""")

		## The capture bonus is paid once per hill (#hp_xp_captured, cleared by load_zone) to the first side to hold it.
		## The hold stream is 1 XP per HOLD_XP_SECONDS, or camping the hill would outpay the whole kill feed of a match.
		alone: dict[int, str] = {
			1: f"if score #hp_red {ns}.data matches 1.. unless score #hp_blue {ns}.data matches 1..",
			2: f"if score #hp_blue {ns}.data matches 1.. unless score #hp_red {ns}.data matches 1..",
		}
		holders: str = f"@a[tag={ns}.in_hp_zone,scores={{{ns}.mp.team=%d,{ns}.mp.in_game=1}}]"
		uncaptured: str = f"if score #hp_xp_captured {ns}.data matches 0"
		due: str = f"if score #hp_xp_hold {ns}.data matches ..0"
		capture_lines: str = "\n".join(
			f'execute {alone[team]} {uncaptured} run tellraw {who} '
			f'[{MGS_TAG},{{"text":"🎯 ","color":"white"}},{{"text":"Hardpoint captured!","color":"gold"}}{suffix}]'
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
# Only an uncontested zone scores.
execute {alone[1]} at @e[tag={ns}.hp_marker] run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute {alone[1]} run scoreboard players add #red {ns}.mp.team 1

execute {alone[2]} at @e[tag={ns}.hp_marker] run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute {alone[2]} run scoreboard players add #blue {ns}.mp.team 1

# First side to hold this hill since it rotated.
{capture_lines}
execute {alone[1]} run scoreboard players set #hp_xp_captured {ns}.data 1
execute {alone[2]} run scoreboard players set #hp_xp_captured {ns}.data 1

# Every {HOLD_XP_SECONDS} s; no message, the bar moving is the feedback.
scoreboard players remove #hp_xp_hold {ns}.data 1
{hold_lines}
execute if score #hp_xp_hold {ns}.data matches ..0 run scoreboard players set #hp_xp_hold {ns}.data {HOLD_XP_SECONDS}

function {ns}:v{version}/multiplayer/check_team_win
""")

		self.sub("rotate", f"""
data remove storage {ns}:multiplayer game.hp_zones[0]

execute unless data storage {ns}:multiplayer game.hp_zones[0] run function {ns}:v{version}/multiplayer/gamemodes/hp/reset_zones

scoreboard players set #hp_rotate_timer {ns}.data 1200
scoreboard players set #hp_rotate_sec {ns}.data 60

function {ns}:v{version}/multiplayer/gamemodes/hp/load_zone
""")

		## Cycle back to the first zone.
		self.sub("reset_zones", f"""
data modify storage {ns}:multiplayer game.hp_zones set from storage {ns}:multiplayer game.map.hardpoint
scoreboard players set #hp_zone_idx {ns}.data 0
""")

		## Like TDM: +1 team.
		self.sub("on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
execute if score @s {ns}.mp.team matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players add #blue {ns}.mp.team 1

function #bs.sidebar:refresh {{objective:"{ns}.sidebar"}}
""")

		self.sub("cleanup", f"""
kill @e[tag={ns}.hp_marker]
kill @e[tag={ns}.hp_label]
tag @a remove {ns}.in_hp_zone
""")

# Functions
def generate_hardpoint() -> None:
	""" Module-level entry point (preserved signature); delegates to :class:`Hardpoint`. """
	Hardpoint()()

