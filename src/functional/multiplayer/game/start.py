""" Starting a game: teams, bounds, spawn markers and the gamemode setup hook. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG
from ...helpers.lifecycle import GameLifecycle
from ..gamemodes.dispatch import gm_dispatch


# Functions
def write_multiplayer_start() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## A map must be loaded first.
	write_versioned_function("multiplayer/start", f"""
{GameLifecycle.game_start_guards(ns, "multiplayer", "Game")}

# Players join a side through Manage Players or + Join.
execute unless entity @a[scores={{{ns}.mp.in_game=1}}] run return run tellraw @s [{MGS_TAG},{{"text":"No players have joined a team. Use Manage Players first.","color":"red"}}]

{GameLifecycle.mode_start_map_bootstrap_lines(ns, "multiplayer", normalize_legacy=True)}

scoreboard players set #red {ns}.mp.team 0
scoreboard players set #blue {ns}.mp.team 0
scoreboard players set #mp_has_boundary {ns}.data 0
scoreboard players set @a {ns}.mp.kills 0
scoreboard players set @a {ns}.mp.deaths 0
scoreboard players set @a {ns}.mp.death_count 0

# Per-match XP for the after-action line; lifetime totals stay.
scoreboard players set @a {ns}.mp.xp_session 0

# Cleared here and re-claimed by the gamemode's setup, so S&D or Demolition never inherit a stale claim.
execute store result score #mp_timer {ns}.data run data get storage {ns}:multiplayer game.time_limit
scoreboard players set #mp_mode_owns_timer {ns}.data 0

# FFA joins everyone; otherwise each player's chosen side, auto-assigning those who opted in without one.
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run team join {ns}.ffa @a[scores={{{ns}.mp.in_game=1}}]
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] if score @s {ns}.mp.team matches 1 run team join {ns}.red @s
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] if score @s {ns}.mp.team matches 2 run team join {ns}.blue @s
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] unless score @s {ns}.mp.team matches 1.. run function {ns}:v{version}/multiplayer/auto_assign_team

tag @a[scores={{{ns}.mp.in_game=1}}] add {ns}.give_class_menu

gamemode adventure @a[scores={{{ns}.mp.in_game=1}}]
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:waypoint_receive_range base set 0.0
gamerule immediate_respawn true
gamerule keep_inventory true

scoreboard players set @a {ns}.mp.spectate_timer 0

{GameLifecycle.regen_enable_lines(ns)}

function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

# Needs 2 points.
execute if data storage {ns}:multiplayer game.map.boundaries[0] if data storage {ns}:multiplayer game.map.boundaries[1] run scoreboard players set #mp_has_boundary {ns}.data 1

execute if score #mp_has_boundary {ns}.data matches 1 run function {ns}:v{version}/shared/load_bounds {{mode:"multiplayer"}}

function {ns}:v{version}/shared/summon_oob {{mode:"multiplayer"}}

function {ns}:v{version}/multiplayer/summon_spawns

# External datapacks can register maps and classes.
function #{ns}:multiplayer/register_maps
function #{ns}:multiplayer/register_classes

function #{ns}:multiplayer/on_game_start

{gm_dispatch(ns, version, "setup")}

# After the entity and setup summons.
execute if data storage {ns}:multiplayer game.map.start_commands[0] run function {ns}:v{version}/shared/run_start_commands {{mode:"multiplayer"}}

# Score limit and initial timer values for the sidebar.
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

scoreboard objectives add {ns}.sidebar dummy
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/refresh_sidebar_ffa
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run function {ns}:v{version}/multiplayer/create_sidebar_team {{title:"Team Deathmatch"}}
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run function {ns}:v{version}/multiplayer/create_sidebar_dom
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run function {ns}:v{version}/multiplayer/create_sidebar_hp
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run function {ns}:v{version}/multiplayer/create_sidebar_snd
execute if data storage {ns}:multiplayer game{{gamemode:"demo"}} run function {ns}:v{version}/multiplayer/create_sidebar_demo

# Kills in the tab list.
scoreboard objectives setdisplay list {ns}.mp.kills

function {ns}:v{version}/multiplayer/tp_all_to_spawns

{GameLifecycle.prep_freeze_lines(ns, "mp")}

# Positive: standard class, negative: custom loadout.
execute as @a[scores={{{ns}.mp.in_game=1}}] at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# `add 0` initializes unset scores, so the `matches 0` test below can succeed.
scoreboard players add @a {ns}.mp.class 0
execute as @a[scores={{{ns}.mp.in_game=1}}] at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default

# Everyone, so classes can change during prep.
execute as @a[scores={{{ns}.mp.in_game=1}}] run function {ns}:v{version}/multiplayer/select_class

# For change detection during prep.
execute as @a[scores={{{ns}.mp.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class

# Prep lasts 10 s.
schedule function {ns}:v{version}/multiplayer/end_prep 200t

tellraw @a ["","⚔ ",[{{"text":"","color":"gold","bold":true}},{{"text":"Preparing"}},"! "],{{"text":"Choose your class! Game starts in 10 seconds!","color":"yellow"}}]
""")

