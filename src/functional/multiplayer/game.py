
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_tag, write_versioned_function


def generate_game() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ============================
	## Scoreboards & Storage Setup
	## ============================
	write_load_file(
f"""
## Multiplayer scoreboards
# Team assignment (1 = red, 2 = blue, 0 = none/spectator)
scoreboard objectives add {ns}.mp.team dummy
# Personal stats
scoreboard objectives add {ns}.mp.kills dummy
scoreboard objectives add {ns}.mp.deaths dummy
# Round timer (ticks remaining)
scoreboard objectives add {ns}.mp.timer dummy

# Initialize team scores (only if not already set)
execute unless score #red {ns}.mp.team matches -2147483648.. run scoreboard players set #red {ns}.mp.team 0
execute unless score #blue {ns}.mp.team matches -2147483648.. run scoreboard players set #blue {ns}.mp.team 0

# Initialize game state
data modify storage {ns}:multiplayer game set value {{state:"lobby",gamemode:"tdm",score_limit:30,time_limit:12000}}
""")

	## ============================
	## Signal function tags
	## ============================
	for event in ["register_maps", "register_classes", "on_game_start", "on_game_end"]:
		write_tag(f"multiplayer/{event}", Mem.ctx.data[ns].function_tags, [])

	## ============================
	## Game Start
	## ============================
	write_versioned_function("multiplayer/start",
f"""
# Initialize game
data modify storage {ns}:multiplayer game.state set value "active"

# Reset scores
scoreboard players set #red {ns}.mp.team 0
scoreboard players set #blue {ns}.mp.team 0
scoreboard players set @a {ns}.mp.kills 0
scoreboard players set @a {ns}.mp.deaths 0
scoreboard players set @a {ns}.mp.death_count 0

# Set timer from time_limit
execute store result score #mp_timer {ns}.data run data get storage {ns}:multiplayer game.time_limit
scoreboard players operation @a {ns}.mp.timer = #mp_timer {ns}.data

# Call register hooks (external datapacks can set up maps/classes)
function #{ns}:multiplayer/register_maps
function #{ns}:multiplayer/register_classes

# Signal game start
function #{ns}:multiplayer/on_game_start

# Give loadout to players who already have a class (positive = standard, negative = custom)
execute as @a at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# For players with no class: auto-apply default custom loadout if set, otherwise show class dialog
execute as @a at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default
execute as @a at @s if score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/select_class

# Announce
tellraw @a ["",{{"text":"⚔ Game Started! ","color":"gold","bold":true}},{{"text":"Pick your class!","color":"yellow"}}]
""")

	## ============================
	## Game Stop
	## ============================
	write_versioned_function("multiplayer/stop",
f"""
# End game
data modify storage {ns}:multiplayer game.state set value "lobby"

# Signal game end
function #{ns}:multiplayer/on_game_end

# Announce scores
tellraw @a ["",{{"text":"⚔ Game Over! ","color":"gold","bold":true}}]
tellraw @a ["",{{"text":"Red","color":"red"}},{{"text":": "}},{{"score":{{"name":"#red","objective":"{ns}.mp.team"}}}}," | ",{{"text":"Blue","color":"blue"}},{{"text":": "}},{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}}}}]

# Clear teams
scoreboard players set @a {ns}.mp.team 0
""")

	## ============================
	## Kill Tracking (Signal Listener)
	## ============================
	write_versioned_function("multiplayer/on_kill_signal",
f"""
# Only process if multiplayer game is active
execute unless data storage {ns}:multiplayer game{{state:"active"}} run return fail

# @s = killer player at this point
scoreboard players add @s {ns}.mp.kills 1

# Update team score based on killer's team
execute if score @s {ns}.mp.team matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players add #blue {ns}.mp.team 1

# Check win condition (score limit)
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score #red {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
""", tags=[f"{ns}:signals/on_kill"])

	## ============================
	## Team Wins
	## ============================
	write_versioned_function("multiplayer/team_wins",
f"""
# Announce winner
$tellraw @a ["",{{"text":"🏆 ","color":"gold"}},{{"text":"$(team) Team Wins!","color":"gold","bold":true}}]
tellraw @a ["",{{"text":"  Final Score - Red: ","color":"gray"}},{{"score":{{"name":"#red","objective":"{ns}.mp.team"}},"color":"red"}},{{"text":" vs Blue: ","color":"gray"}},{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}},"color":"blue"}}]

# End game
function {ns}:v{version}/multiplayer/stop
""")
