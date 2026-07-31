""" Starting a game: teams, bounds, spawn markers and the gamemode setup hook. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG
from ...helpers.lifecycle import GameLifecycle
from ..gamemodes.dispatch import gm_dispatch


# Functions
def write_multiplayer_start() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Game Start (requires a map to be loaded first)
	write_versioned_function("multiplayer/start", f"""
# Prevent starting if already active or preparing
{GameLifecycle.game_start_guards(ns, "multiplayer", "Game")}

# Require at least one opted-in player (players are independent until assigned via Manage Players / + Join)
execute unless entity @a[scores={{{ns}.mp.in_game=1}}] run return run tellraw @s [{MGS_TAG},{{"text":"No players have joined a team — use Manage Players first.","color":"red"}}]

{GameLifecycle.mode_start_map_bootstrap_lines(ns, "multiplayer", True)}

# Teams setup
team add {ns}.red
team modify {ns}.red color red
team modify {ns}.red friendlyFire false
team modify {ns}.red nametagVisibility hideForOtherTeams
team add {ns}.blue
team modify {ns}.blue color blue
team modify {ns}.blue friendlyFire false
team modify {ns}.blue nametagVisibility hideForOtherTeams
team add {ns}.ffa
team modify {ns}.ffa color yellow
team modify {ns}.ffa friendlyFire true
team modify {ns}.ffa nametagVisibility never

# Reset scores
scoreboard players set #red {ns}.mp.team 0
scoreboard players set #blue {ns}.mp.team 0
scoreboard players set #mp_has_boundary {ns}.data 0
scoreboard players set @a {ns}.mp.kills 0
scoreboard players set @a {ns}.mp.deaths 0
scoreboard players set @a {ns}.mp.death_count 0

# Per-match XP, for the after-action line. The lifetime totals are deliberately NOT touched.
scoreboard players set @a {ns}.mp.xp_session 0

# Set timer from time_limit. Cleared here and re-claimed by the gamemode's own setup below, so a mode that
# drives its own clock (S&D, Demolition) cannot inherit a stale claim from the previous match.
execute store result score #mp_timer {ns}.data run data get storage {ns}:multiplayer game.time_limit
scoreboard players set #mp_mode_owns_timer {ns}.data 0

# Assign vanilla teams to opted-in players only: FFA joins everyone; otherwise honor each player's
# chosen side (set via Manage Players), auto-assigning anyone who opted in without picking a team.
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run team join {ns}.ffa @a[scores={{{ns}.mp.in_game=1}}]
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] if score @s {ns}.mp.team matches 1 run team join {ns}.red @s
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] if score @s {ns}.mp.team matches 2 run team join {ns}.blue @s
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] unless score @s {ns}.mp.team matches 1.. run function {ns}:v{version}/multiplayer/auto_assign_team

# Enable class menu for multiplayer players
tag @a[scores={{{ns}.mp.in_game=1}}] add {ns}.give_class_menu

# Set all in-game players to adventure and enable instant respawn
gamemode adventure @a[scores={{{ns}.mp.in_game=1}}]
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:waypoint_receive_range base set 0.0
gamerule immediate_respawn true
gamerule keep_inventory true

# Reset spectate timers
scoreboard players set @a {ns}.mp.spectate_timer 0

{GameLifecycle.regen_enable_lines(ns)}

# Store base coordinates for offset
function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

# Detect whether this map defines a boundary (needs 2 points)
execute if data storage {ns}:multiplayer game.map.boundaries[0] if data storage {ns}:multiplayer game.map.boundaries[1] run scoreboard players set #mp_has_boundary {ns}.data 1

# Normalize and store boundaries only when they exist
execute if score #mp_has_boundary {ns}.data matches 1 run function {ns}:v{version}/shared/load_bounds {{mode:"multiplayer"}}

# Summon out-of-bounds markers
function {ns}:v{version}/shared/summon_oob {{mode:"multiplayer"}}

# Summon spawn point markers (for smart spawn selection)
function {ns}:v{version}/multiplayer/summon_spawns

# Call register hooks (external datapacks can set up maps/classes)
function #{ns}:multiplayer/register_maps
function #{ns}:multiplayer/register_classes

# Signal game start
function #{ns}:multiplayer/on_game_start

# Run gamemode-specific setup
{gm_dispatch(ns, version, "setup")}

# Run map-defined start commands after entity/setup summons
execute if data storage {ns}:multiplayer game.map.start_commands[0] run function {ns}:v{version}/shared/run_start_commands {{mode:"multiplayer"}}

# Store score limit and compute initial timer values for sidebar
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute store result score #timer_sec {ns}.data run scoreboard players get #mp_timer {ns}.data
scoreboard players operation #timer_sec {ns}.data /= #20 {ns}.data
execute store result score #timer_min {ns}.data run scoreboard players get #timer_sec {ns}.data
scoreboard players operation #timer_min {ns}.data /= #60 {ns}.data
scoreboard players operation #timer_mod {ns}.data = #timer_sec {ns}.data
scoreboard players operation #timer_mod {ns}.data %= #60 {ns}.data
scoreboard players operation #timer_tens {ns}.data = #timer_mod {ns}.data
scoreboard players operation #timer_tens {ns}.data /= #10 {ns}.data
scoreboard players operation #timer_ones {ns}.data = #timer_mod {ns}.data
scoreboard players operation #timer_ones {ns}.data %= #10 {ns}.data

# Create sidebar HUD
scoreboard objectives add {ns}.sidebar dummy
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/refresh_sidebar_ffa
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run function {ns}:v{version}/multiplayer/create_sidebar_team {{title:"Team Deathmatch"}}
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run function {ns}:v{version}/multiplayer/create_sidebar_dom
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run function {ns}:v{version}/multiplayer/create_sidebar_hp
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run function {ns}:v{version}/multiplayer/create_sidebar_snd
execute if data storage {ns}:multiplayer game{{gamemode:"demo"}} run function {ns}:v{version}/multiplayer/create_sidebar_demo

# Show kills in player list (tab)
scoreboard objectives setdisplay list {ns}.mp.kills

# Teleport players to spawn points
function {ns}:v{version}/multiplayer/tp_all_to_spawns

# Freeze all players (no movement during prep)
{GameLifecycle.prep_freeze_lines(ns, "mp")}

# Give loadout to players who already have a class (positive = standard, negative = custom)
execute as @a[scores={{{ns}.mp.in_game=1}}] at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# For players with no class: auto-apply default custom loadout if set
# (add 0 initializes unset scores so the 'matches 0' check below can succeed)
scoreboard players add @a {ns}.mp.class 0
execute as @a[scores={{{ns}.mp.in_game=1}}] at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default

# Show class selection dialog to EVERYONE (so they can change during prep)
execute as @a[scores={{{ns}.mp.in_game=1}}] run function {ns}:v{version}/multiplayer/select_class

# Store current class for change detection during prep
execute as @a[scores={{{ns}.mp.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class

# Schedule end of prep (10 seconds = 200 ticks)
schedule function {ns}:v{version}/multiplayer/end_prep 200t

# Announce
tellraw @a ["","⚔ ",[{{"text":"","color":"gold","bold":true}},{{"text":"Preparing"}},"! "],{{"text":"Choose your class! Game starts in 10 seconds!","color":"yellow"}}]
""")

