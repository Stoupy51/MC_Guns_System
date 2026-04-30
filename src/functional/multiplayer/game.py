
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_tag, write_tick_file, write_versioned_function

from ..core.respawn_countdown import respawn_countdown_tick_lines
from ..helpers import MGS_TAG, game_start_guards, regen_disable_lines, regen_enable_lines


def generate_game() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Scoreboards & Storage Setup
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
# In-game tag scoreboard (1 = in active game)
scoreboard objectives add {ns}.mp.in_game dummy

# Boundary checking coords
scoreboard objectives add {ns}.mp.bx dummy
scoreboard objectives add {ns}.mp.by dummy
scoreboard objectives add {ns}.mp.bz dummy

# Class change detection (for prep phase)
scoreboard objectives add {ns}.mp.prev_class dummy

# Spectate timer (ticks remaining before respawn, 0 = not spectating)
scoreboard objectives add {ns}.mp.spectate_timer dummy

# FFA ranking (1 = most kills, 2 = second, ..., 0 = unranked)
scoreboard objectives add {ns}.mp.ffa_rank dummy

# Initialize team scores (only if not already set)
execute unless score #red {ns}.mp.team matches -2147483648.. run scoreboard players set #red {ns}.mp.team 0
execute unless score #blue {ns}.mp.team matches -2147483648.. run scoreboard players set #blue {ns}.mp.team 0

# Initialize game state (only if not yet set)
execute unless data storage {ns}:multiplayer game run data modify storage {ns}:multiplayer game set value {{state:"lobby",gamemode:"tdm",score_limit:30,time_limit:12000,map_id:"hijacked"}}

""")

	## Signal function tags
	for event in ["register_maps", "register_classes", "on_game_start", "on_game_end"]:
		write_tag(f"multiplayer/{event}", Mem.ctx.data[ns].function_tags, [])

	## Game Start (requires a map to be loaded first)
	write_versioned_function("multiplayer/start", f"""
# Prevent starting if already active or preparing
{game_start_guards(ns, "multiplayer", "Game")}

# Load the selected map (reads map_id from game storage)
function {ns}:v{version}/multiplayer/load_map_from_storage with storage {ns}:multiplayer game
execute unless score #map_load_found {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"No map found! Select a map first.","color":"red"}}]

# Copy loaded map data into game state
data modify storage {ns}:multiplayer game.map set from storage {ns}:temp map_load.result

# Legacy compatibility: normalize respawn command keys
execute unless data storage {ns}:multiplayer game.map.respawn_commands if data storage {ns}:multiplayer game.map.respawn_command[0] run data modify storage {ns}:multiplayer game.map.respawn_commands set from storage {ns}:multiplayer game.map.respawn_command
execute unless data storage {ns}:multiplayer game.map.respawn_commands if data storage {ns}:multiplayer game.map.respawn_command.command run data modify storage {ns}:multiplayer game.map.respawn_commands set value []
execute unless data storage {ns}:multiplayer game.map.respawn_commands[0] if data storage {ns}:multiplayer game.map.respawn_command.command run data modify storage {ns}:multiplayer game.map.respawn_commands append from storage {ns}:multiplayer game.map.respawn_command
execute unless data storage {ns}:multiplayer game.map.respawn_commands run data modify storage {ns}:multiplayer game.map.respawn_commands set value []
execute unless data storage {ns}:multiplayer game.map.start_commands run data modify storage {ns}:multiplayer game.map.start_commands set value []

# Initialize game
data modify storage {ns}:multiplayer game.state set value "preparing"

# Reset scores
scoreboard players set #red {ns}.mp.team 0
scoreboard players set #blue {ns}.mp.team 0
scoreboard players set #mp_has_boundary {ns}.data 0
scoreboard players set @a {ns}.mp.kills 0
scoreboard players set @a {ns}.mp.deaths 0
scoreboard players set @a {ns}.mp.death_count 0

# Set timer from time_limit
execute store result score #mp_timer {ns}.data run data get storage {ns}:multiplayer game.time_limit

# Tag all non-spectator players as in-game
scoreboard players set @a {ns}.mp.in_game 1

# Auto-assign teamless players so every participant has a team
execute as @a[scores={{{ns}.mp.in_game=1}}] unless score @s {ns}.mp.team matches 1.. run function {ns}:v{version}/multiplayer/auto_assign_team

# Enable class menu for multiplayer players
tag @a[scores={{{ns}.mp.in_game=1}}] add {ns}.give_class_menu

# Set all in-game players to adventure and enable instant respawn
gamemode adventure @a[scores={{{ns}.mp.in_game=1}}]
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:waypoint_receive_range base set 0.0
gamerule immediate_respawn true
gamerule keep_inventory true

# Reset spectate timers
scoreboard players set @a {ns}.mp.spectate_timer 0

{regen_enable_lines(ns)}

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
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/gamemodes/ffa/setup
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run function {ns}:v{version}/multiplayer/gamemodes/tdm/setup
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run function {ns}:v{version}/multiplayer/gamemodes/dom/setup
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run function {ns}:v{version}/multiplayer/gamemodes/hp/setup
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run function {ns}:v{version}/multiplayer/gamemodes/snd/setup

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
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/create_sidebar_ffa
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run function {ns}:v{version}/multiplayer/create_sidebar_team {{title:"Team Deathmatch"}}
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run function {ns}:v{version}/multiplayer/create_sidebar_dom
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run function {ns}:v{version}/multiplayer/create_sidebar_hp
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run function {ns}:v{version}/multiplayer/create_sidebar_team {{title:"Search & Destroy"}}

# Show kills in player list (tab)
scoreboard objectives setdisplay list {ns}.mp.kills

# Teleport players to spawn points
function {ns}:v{version}/multiplayer/tp_all_to_spawns

# Freeze all players (no movement during prep)
effect give @a[scores={{{ns}.mp.in_game=1}}] darkness 25 255 true
effect give @a[scores={{{ns}.mp.in_game=1}}] blindness 25 255 true
effect give @a[scores={{{ns}.mp.in_game=1}}] night_vision 25 255 true
effect give @a[scores={{{ns}.mp.in_game=1}}] saturation infinite 255 true
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:jump_strength base set 0

# Give loadout to players who already have a class (positive = standard, negative = custom)
execute as @a[scores={{{ns}.mp.in_game=1}}] at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# For players with no class: auto-apply default custom loadout if set
scoreboard players add @s {ns}.mp.class 0
execute as @a[scores={{{ns}.mp.in_game=1}}] at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default

# Show class selection dialog to EVERYONE (so they can change during prep)
execute as @a[scores={{{ns}.mp.in_game=1}}] run function {ns}:v{version}/multiplayer/select_class

# Store current class for change detection during prep
execute as @a[scores={{{ns}.mp.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class

# Schedule end of prep (10 seconds = 200 ticks)
schedule function {ns}:v{version}/multiplayer/end_prep 200t

# Announce
tellraw @a ["",[{{"text":"","color":"gold","bold":true}},"⚔ ",{{"text":"Preparing"}},"! "],{{"text":"Choose your class! Game starts in 10 seconds!","color":"yellow"}}]
""")

	## Load map from storage (reads map_id from game state and passes to load macro)
	write_versioned_function("multiplayer/load_map_from_storage", f"""
$function {ns}:v{version}/shared/maps/load {{id:"$(map_id)",mode:"multiplayer",override:{{}}}}
""")

	## Game Stop
	write_versioned_function("multiplayer/stop", f"""
# End game
data modify storage {ns}:multiplayer game.state set value "lobby"

# Cancel scheduled prep end (in case game stopped during prep)
schedule clear {ns}:v{version}/multiplayer/end_prep

# Restore movement (in case stopped during prep)
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:jump_strength base set 0.42

# Clear prep effects (in case stopped during prep)
effect clear @a[scores={{{ns}.mp.in_game=1}}] darkness
effect clear @a[scores={{{ns}.mp.in_game=1}}] blindness
effect clear @a[scores={{{ns}.mp.in_game=1}}] night_vision

# Gamemode cleanup
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/gamemodes/ffa/cleanup
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run function {ns}:v{version}/multiplayer/gamemodes/tdm/cleanup
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run function {ns}:v{version}/multiplayer/gamemodes/dom/cleanup
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run function {ns}:v{version}/multiplayer/gamemodes/hp/cleanup
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run function {ns}:v{version}/multiplayer/gamemodes/snd/cleanup

{regen_disable_lines(ns)}

# Restore all spectating players to adventure mode
gamemode adventure @a[scores={{{ns}.mp.in_game=1}},gamemode=spectator]

# Kill gamemode entities
kill @e[tag={ns}.gm_entity]

# Signal game end
function #{ns}:multiplayer/on_game_end

# Announce scores
tellraw @a ["",[{{"text":"","color":"gold","bold":true}},"⚔ ",{{"text":"Game Over"}},"! "]]
tellraw @a ["",{{"text":"Red","color":"red"}},{{"text":": "}},{{"score":{{"name":"#red","objective":"{ns}.mp.team"}}}}," | ",{{"text":"Blue","color":"blue"}},{{"text":": "}},{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}}}}]

# Remove sidebar and list displays
scoreboard objectives setdisplay sidebar
scoreboard objectives remove {ns}.sidebar
scoreboard objectives setdisplay list

# Clear in-game state
team leave @a[team={ns}.red]
team leave @a[team={ns}.blue]
scoreboard players set @a {ns}.mp.in_game 0
scoreboard players set @a {ns}.mp.team 0
scoreboard players set @a {ns}.mp.spectate_timer 0
scoreboard players set #mp_has_boundary {ns}.data 0
tag @a[tag={ns}.give_class_menu] remove {ns}.give_class_menu
""")

	## Join Ongoing Game (late-joiner support)
	write_versioned_function("multiplayer/join_game", f"""
# Require an active or preparing game
execute unless data storage {ns}:multiplayer game{{state:"active"}} unless data storage {ns}:multiplayer game{{state:"preparing"}} run return run tellraw @s [{MGS_TAG},{{"text":"No active game to join!","color":"red"}}]

# Prevent double-joining
execute if score @s {ns}.mp.in_game matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"You are already in the game!","color":"red"}}]

# Tag as in-game and reset stats
scoreboard players set @s {ns}.mp.in_game 1
scoreboard players set @s {ns}.mp.kills 0
scoreboard players set @s {ns}.mp.deaths 0
scoreboard players set @s {ns}.mp.death_count 0
scoreboard players set @s {ns}.mp.spectate_timer 0

# Auto-assign team if not already on one
execute unless score @s {ns}.mp.team matches 1.. run function {ns}:v{version}/multiplayer/auto_assign_team

# Setup player (match active game settings)
gamemode adventure @s
attribute @s minecraft:waypoint_receive_range base set 0.0
effect give @s saturation infinite 255 true

# Enable class menu and show class selection
tag @s add {ns}.give_class_menu
function {ns}:v{version}/multiplayer/select_class

# Apply class if already chosen
execute unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# Teleport to spawn
function {ns}:v{version}/multiplayer/respawn_tp

# Announce
tellraw @a ["",{{"selector":"@s","color":"yellow"}},{{"text":" joined the game!","color":"yellow"}}]
""")

	# Simulated Death ───────────────────────────────────────────
	# Called when lethal damage is intercepted (bullet/projectile) or for OOB kills
	# @s = victim player; storage mgs:input with.attacker may or may not exist

	write_versioned_function("multiplayer/simulate_death", f"""
# Heal to prevent actual death & Increment death stats
effect give @s instant_health 1 100 true
scoreboard players add @s {ns}.mp.deaths 1

# Fire damage signal (hit effects, hitmarker, DPS) if this came from a bullet hit
execute if data storage {ns}:input with.amount run function #{ns}:signals/damage with storage {ns}:input with

# Fire kill signal as attacker (if attacker exists in input)
execute if data storage {ns}:input with.attacker run function {ns}:v{version}/multiplayer/simulate_death_fire_kill with storage {ns}:input with

# No attacker: random funny self-death message
execute unless data storage {ns}:input with.attacker run function {ns}:v{version}/multiplayer/random_death_message

# Increment death stats
scoreboard players add @s {ns}.mp.deaths 1

# S&D: no respawning, mark as dead and go spectator
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run return run function {ns}:v{version}/multiplayer/gamemodes/snd/on_death

# Set player to spectator mode for 3 seconds (60 ticks)
gamemode spectator @s
scoreboard players set @s {ns}.mp.spectate_timer 60

# Spectate attacker (tagged by fire_kill) or random
spectate @p[tag={ns}.temp_killer,gamemode=!spectator] @s
execute unless entity @a[tag={ns}.temp_killer] run function {ns}:v{version}/multiplayer/spectate_random_player
tag @a[tag={ns}.temp_killer] remove {ns}.temp_killer

# Announce death & playsound
title @s title [{{"text":"☠","color":"red"}}]
title @s subtitle [{{"text":"Respawning in 3 seconds...","color":"gray"}}]
execute at @s run playsound minecraft:entity.player.hurt ambient @s
""")

	## Fire kill signal as attacker + death message (macro function)
	## @s = victim, $(attacker) = attacker selector from storage
	write_versioned_function("multiplayer/simulate_death_fire_kill", f"""
$tag $(attacker) add {ns}.temp_killer

# Self-kill check: if victim(@s) is also tagged as killer, it's self-damage
execute if entity @s[tag={ns}.temp_killer] run tag @s remove {ns}.temp_killer
execute unless entity @a[tag={ns}.temp_killer] run return run function {ns}:v{version}/multiplayer/random_self_kill_message

# Normal kill: fire signal and show message
tag @s add {ns}.temp_victim
$execute as $(attacker) run function #{ns}:signals/on_kill
function {ns}:v{version}/multiplayer/random_kill_message
tag @s remove {ns}.temp_victim
""")

	## Random death message for self-deaths (OOB, environmental)
	write_versioned_function("multiplayer/random_death_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s","color":"red"}}," ",{{"text":"made a terrible mistake","color":"gray"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s","color":"red"}}," ",{{"text":"forgot how gravity works","color":"gray"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s","color":"red"}}," ",{{"text":"played themselves","color":"gray"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s","color":"red"}}," ",{{"text":"left the battlefield","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s","color":"red"}}," ",{{"text":"embraced the void","color":"gray"}}]
""")

	## Random self-kill message (grenade, RPG, own explosion)
	write_versioned_function("multiplayer/random_self_kill_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s","color":"red"}}," ",{{"text":"blew themselves up","color":"gray"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s","color":"red"}}," ",{{"text":"got a taste of their own medicine","color":"gray"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s","color":"red"}}," ",{{"text":"found out the blast radius the hard way","color":"gray"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s","color":"red"}}," ",{{"text":"didn't throw the grenade far enough","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s","color":"red"}}," ",{{"text":"is their own worst enemy","color":"gray"}}]
""")

	## Random kill message (uses temp_killer/temp_victim tags, shared by simulate_death + on_respawn)
	write_versioned_function("multiplayer/random_kill_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]","color":"red"}}," ",{{"text":"eliminated","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]","color":"red"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]","color":"red"}}," ",{{"text":"took down","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]","color":"red"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]","color":"red"}}," ",{{"text":"dispatched","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]","color":"red"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]","color":"red"}}," ",{{"text":"sent","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]","color":"red"}}," ",{{"text":"to the shadow realm","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]","color":"red"}}," ",{{"text":"wiped","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]","color":"red"}}," ",{{"text":"off the map","color":"gray"}}]
""")

	## Kill Tracking (Signal Listener) - now dispatches to gamemode
	write_versioned_function("multiplayer/on_kill_signal", f"""
# Only process if multiplayer game is active
execute unless data storage {ns}:multiplayer game{{state:"active"}} run return fail

# Dispatch to gamemode-specific kill handler
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run return run function {ns}:v{version}/multiplayer/gamemodes/ffa/on_kill
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run return run function {ns}:v{version}/multiplayer/gamemodes/tdm/on_kill
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run return run function {ns}:v{version}/multiplayer/gamemodes/dom/on_kill
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run return run function {ns}:v{version}/multiplayer/gamemodes/hp/on_kill
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run return run function {ns}:v{version}/multiplayer/gamemodes/snd/on_kill
""", tags=[f"{ns}:signals/on_kill"])

	## Check Team Win (shared by TDM, DOM, HP)
	write_versioned_function("multiplayer/check_team_win", f"""
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score #red {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
""")

	## Team Wins
	write_versioned_function("multiplayer/team_wins", f"""
# Announce winner
$tellraw @a ["",{{"text":"🏆 ","color":"gold"}},{{"text":"$(team) Team Wins!","color":"gold","bold":true}}]
tellraw @a ["",[{{"text":"","color":"gray"}},"  ",{{"text":"Final Score - Red"}},": "],{{"score":{{"name":"#red","objective":"{ns}.mp.team"}},"color":"red"}},[{{"text":"","color":"gray"}}," ",{{"text":"vs Blue"}},": "],{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}},"color":"blue"}}]

# End game
function {ns}:v{version}/multiplayer/stop
""")

	# Game Tick (runs once per server tick when game is active)
	write_tick_file(f"""
# Multiplayer game tick
execute if data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/game_tick
execute if data storage {ns}:multiplayer game{{state:"preparing"}} run function {ns}:v{version}/multiplayer/prep_tick
""")

	write_versioned_function("multiplayer/game_tick", f"""
{respawn_countdown_tick_lines(ns, "mp", f"{ns}:v{version}/multiplayer/actual_respawn")}

# Timer
scoreboard players remove #mp_timer {ns}.data 1

# Timer display every second (20 ticks)
execute store result score #tick_mod {ns}.data run scoreboard players get #mp_timer {ns}.data
scoreboard players operation #tick_mod {ns}.data %= #20 {ns}.data
execute if score #tick_mod {ns}.data matches 0 run function {ns}:v{version}/multiplayer/timer_display

# Time's up
execute if score #mp_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/time_up

# Boundary enforcement (skip players with respawn protection)
execute if score #mp_has_boundary {ns}.data matches 1 as @e[type=player,scores={{{ns}.mp.in_game=1,{ns}.mp.death_count=0}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/multiplayer/check_bounds

# Out-of-bounds check (skip players with respawn protection)
execute as @e[type=player,scores={{{ns}.mp.in_game=1,{ns}.mp.death_count=0}},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag={ns}.oob_point,distance=..5] run function {ns}:v{version}/multiplayer/oob_kill

# Gamemode tick dispatch
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/gamemodes/ffa/tick
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run function {ns}:v{version}/multiplayer/gamemodes/tdm/tick
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run function {ns}:v{version}/multiplayer/gamemodes/dom/tick
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run function {ns}:v{version}/multiplayer/gamemodes/hp/tick
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run function {ns}:v{version}/multiplayer/gamemodes/snd/tick
""")

	## Timer display (actionbar timer in minutes:seconds for all in-game players)
	write_versioned_function("multiplayer/timer_display", f"""
# Convert ticks to seconds
execute store result score #timer_sec {ns}.data run scoreboard players get #mp_timer {ns}.data
scoreboard players operation #timer_sec {ns}.data /= #20 {ns}.data
execute store result score #timer_min {ns}.data run scoreboard players get #timer_sec {ns}.data
scoreboard players operation #timer_min {ns}.data /= #60 {ns}.data
scoreboard players operation #timer_mod {ns}.data = #timer_sec {ns}.data
scoreboard players operation #timer_mod {ns}.data %= #60 {ns}.data

# Zero-padded seconds for sidebar
scoreboard players operation #timer_tens {ns}.data = #timer_mod {ns}.data
scoreboard players operation #timer_tens {ns}.data /= #10 {ns}.data
scoreboard players operation #timer_ones {ns}.data = #timer_mod {ns}.data
scoreboard players operation #timer_ones {ns}.data %= #10 {ns}.data

# Refresh sidebar with updated values
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function #bs.sidebar:refresh {{objective:"{ns}.sidebar"}}
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/refresh_sidebar_ffa
""")

	## Time up → determine winner
	write_versioned_function("multiplayer/time_up", f"""
# FFA: player with most kills wins
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/ffa_time_up

# Team modes: team with more points wins
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} if score #red {ns}.mp.team > #blue {ns}.mp.team run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} if score #blue {ns}.mp.team > #red {ns}.mp.team run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} if score #red {ns}.mp.team = #blue {ns}.mp.team run function {ns}:v{version}/multiplayer/game_draw
""")

	## FFA time up: find player with most kills
	write_versioned_function("multiplayer/ffa_time_up", f"""
tellraw @a [{MGS_TAG},{{"text":"Time's up!","color":"gold"}}]

# Store max kills into a score
scoreboard players set #max_kills {ns}.data 0
scoreboard players operation #max_kills {ns}.data > @a[scores={{{ns}.mp.in_game=1}}] {ns}.mp.kills

# The player with that score wins
execute as @a[scores={{{ns}.mp.in_game=1}}] if score @s {ns}.mp.kills = #max_kills {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/ffa/player_wins
""")

	## Game draw
	write_versioned_function("multiplayer/game_draw", f"""
tellraw @a ["",{{"text":"🤝 ","color":"gold"}},{{"text":"Draw!","color":"gold","bold":true}}]
function {ns}:v{version}/multiplayer/stop
""")

	## Boundary check (run as each in-game player at their position)
	write_versioned_function("multiplayer/check_bounds", f"""
# Get player position as integers
data modify storage {ns}:temp _player_pos set from entity @s Pos
execute store result score @s {ns}.mp.bx run data get storage {ns}:temp _player_pos[0]
execute store result score @s {ns}.mp.by run data get storage {ns}:temp _player_pos[1]
execute store result score @s {ns}.mp.bz run data get storage {ns}:temp _player_pos[2]

# Check if outside boundaries (any axis out of range = OOB)
execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
""")

	## Kill player out of bounds (simulate death, never /kill)
	write_versioned_function("multiplayer/bounds_kill", f"""
# Clear attacker input (environmental death) and simulate death
data modify storage {ns}:input with set value {{}}
function {ns}:v{version}/multiplayer/simulate_death
""")

	## OOB kill (player near an out-of-bounds marker) (simulate death, never /kill)
	write_versioned_function("multiplayer/oob_kill", f"""
# Clear attacker input (environmental death) and simulate death
data modify storage {ns}:input with set value {{}}
function {ns}:v{version}/multiplayer/simulate_death
""")

	# Spawn Point Markers ───────────────────────────────────────

	## Summon spawn markers from map data (called at game start)
	write_versioned_function("multiplayer/summon_spawns", f"""
# Red spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:multiplayer game.map.spawning_points.red
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_red"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/multiplayer/summon_spawn_iter

# Blue spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:multiplayer game.map.spawning_points.blue
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_blue"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/multiplayer/summon_spawn_iter

# General spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:multiplayer game.map.spawning_points.general
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_general"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/multiplayer/summon_spawn_iter
""")

	write_versioned_function("multiplayer/summon_spawn_iter", f"""
# Read relative coords
execute store result score #sx {ns}.data run data get storage {ns}:temp _spawn_iter[0][0]
execute store result score #sy {ns}.data run data get storage {ns}:temp _spawn_iter[0][1]
execute store result score #sz {ns}.data run data get storage {ns}:temp _spawn_iter[0][2]
execute store result score #syaw {ns}.data run data get storage {ns}:temp _spawn_iter[0][3] 100

# Convert to absolute
scoreboard players operation #sx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #sy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #sz {ns}.data += #gm_base_z {ns}.data

# Store position + yaw for macro
execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #sx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #sy {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #sz {ns}.data
execute store result storage {ns}:temp _spos.yaw double 0.01 run scoreboard players get #syaw {ns}.data
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_tag

# Summon
function {ns}:v{version}/multiplayer/summon_spawn_at with storage {ns}:temp _spos

# Next
data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/multiplayer/summon_spawn_iter
""")

	write_versioned_function("multiplayer/summon_spawn_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.spawn_point","$(tag)","{ns}.gm_entity"],data:{{yaw:$(yaw)}}}}
""")

	# Smart Spawn Selection ─────────────────────────────────────

	## TP all players to spawn points at game start
	write_versioned_function("multiplayer/tp_all_to_spawns", f"""
# FFA: everyone uses general spawns
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}

# Team modes: TP by team
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=2}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}

# Players with no team: use general spawns
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=0}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}

# Clean up used spawn markers
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

	## Pick best spawn: find spawn marker farthest from any enemy player (run as player)
	write_versioned_function("multiplayer/pick_spawn", f"""
# Mark this player as needing a spawn
tag @s add {ns}.spawn_pending

# Tag enemy players (for distance calculation — ignore teammates)
# In FFA or team=0: all in-game players are "enemies" for spawn distance
execute if score @s {ns}.mp.team matches 0 run tag @a[scores={{{ns}.mp.in_game=1}}] add {ns}.spawn_enemy
# In team modes: only tag players on different teams
execute if score @s {ns}.mp.team matches 1 run tag @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=2..}}] add {ns}.spawn_enemy
execute if score @s {ns}.mp.team matches 2 run tag @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=..1}}] add {ns}.spawn_enemy
# Never count self as an enemy
tag @s remove {ns}.spawn_enemy

# Tag candidate spawn markers of the right type (exclude already-used spawns)
$tag @e[tag={ns}.spawn_point,tag={ns}.spawn_$(type),tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# Remove candidates that have an enemy player within 5 blocks
execute as @e[tag={ns}.spawn_candidate] at @s if entity @a[tag={ns}.spawn_enemy,distance=..5] run tag @s remove {ns}.spawn_candidate

# If all were removed (all spawns used or contested), re-tag all as candidates
$execute unless entity @e[tag={ns}.spawn_candidate] run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_$(type)] add {ns}.spawn_candidate

# If no enemies, pick random candidate directly (skip expensive distance calc)
execute unless entity @a[tag={ns}.spawn_enemy] run return run function {ns}:v{version}/multiplayer/pick_spawn_random

# Limit to X random candidates before distance computation (optimization)
tag @e[tag={ns}.spawn_candidate,sort=random,limit=32] add {ns}.spawn_final
tag @e[tag={ns}.spawn_candidate,tag=!{ns}.spawn_final] remove {ns}.spawn_candidate
tag @e[tag={ns}.spawn_final] remove {ns}.spawn_final

# Compute distance² to nearest enemy player for each candidate
execute as @e[tag={ns}.spawn_candidate] at @s run function {ns}:v{version}/multiplayer/spawn_calc_dist

# Find the maximum distance score
scoreboard players set #best_dist {ns}.data 0
scoreboard players operation #best_dist {ns}.data > @e[tag={ns}.spawn_candidate] {ns}.data

# Pick the first candidate with that best score and TP the pending player there
execute as @e[tag={ns}.spawn_candidate,sort=random] if score @s {ns}.data = #best_dist {ns}.data run function {ns}:v{version}/multiplayer/tp_to_spawn

# Clean up
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
tag @a[tag={ns}.spawn_enemy] remove {ns}.spawn_enemy
""")

	## Pick random spawn (no enemies — skip distance calc entirely)
	write_versioned_function("multiplayer/pick_spawn_random", f"""
execute as @n[tag={ns}.spawn_candidate,sort=random] run function {ns}:v{version}/multiplayer/tp_to_spawn

# Clean up
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
tag @a[tag={ns}.spawn_enemy] remove {ns}.spawn_enemy
""")

	## Calculate distance² from spawn marker to nearest enemy player (run as marker at marker)
	write_versioned_function("multiplayer/spawn_calc_dist", f"""
# Get marker position
execute store result score #mx {ns}.data run data get entity @s Pos[0]
execute store result score #my {ns}.data run data get entity @s Pos[1]
execute store result score #mz {ns}.data run data get entity @s Pos[2]

# Get nearest enemy player position (expensive — caller limits candidates)
data modify storage {ns}:temp _nearest set from entity @p[tag={ns}.spawn_enemy] Pos
execute store result score #px {ns}.data run data get storage {ns}:temp _nearest[0]
execute store result score #py {ns}.data run data get storage {ns}:temp _nearest[1]
execute store result score #pz {ns}.data run data get storage {ns}:temp _nearest[2]

# dx, dy, dz
scoreboard players operation #mx {ns}.data -= #px {ns}.data
scoreboard players operation #my {ns}.data -= #py {ns}.data
scoreboard players operation #mz {ns}.data -= #pz {ns}.data

# distance² = dx² + dy² + dz²
scoreboard players operation #mx {ns}.data *= #mx {ns}.data
scoreboard players operation #my {ns}.data *= #my {ns}.data
scoreboard players operation #mz {ns}.data *= #mz {ns}.data
scoreboard players operation #mx {ns}.data += #my {ns}.data
scoreboard players operation #mx {ns}.data += #mz {ns}.data

# Store on entity
scoreboard players operation @s {ns}.data = #mx {ns}.data
""")

	## TP player to chosen spawn marker (run as the marker)
	write_versioned_function("multiplayer/tp_to_spawn", f"""
# Store marker position and yaw for macro
execute store result storage {ns}:temp _tp.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _tp.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _tp.z double 1 run data get entity @s Pos[2]
data modify storage {ns}:temp _tp.yaw set from entity @s data.yaw

# TP the pending player
execute as @p[tag={ns}.spawn_pending] run function {ns}:v{version}/multiplayer/tp_player_at with storage {ns}:temp _tp

# Mark this spawn as used (prevents duplicate assignments) (only in preparing time)
execute unless data storage {ns}:multiplayer game{{state:"active"}} run tag @s add {ns}.spawn_used
""")

	## TP macro (run as the player to TP)
	write_versioned_function("multiplayer/tp_player_at", "$tp @s $(x) $(y) $(z) $(yaw) 0")

	## Respawn TP: use general spawns on respawn to prevent spawn camping (run as the respawning player)
	write_versioned_function("multiplayer/respawn_tp", f"""
# Try general spawns first (prevents spawn camping)
execute if entity @e[tag={ns}.spawn_point,tag={ns}.spawn_general] run return run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}

# Fallback to team spawns if map has no general spawns
execute if score @s {ns}.mp.team matches 1 run return run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute if score @s {ns}.mp.team matches 2 run return run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}
""")

	# Sidebar HUD ───────────────────────────────────────────────

	# Build sidebar content components for reuse
	sb_timer = (
		f'[{{text:" ⏱ ",color:"yellow"}},'
		f'[{{score:{{name:"#timer_min",objective:"{ns}.data"}},"color":"yellow"}},'
		f'{{text:":"}},'
		f'{{score:{{name:"#timer_tens",objective:"{ns}.data"}}}},'
		f'{{score:{{name:"#timer_ones",objective:"{ns}.data"}}}}]]'
	)
	sb_red = f'[[{{text:" 🔴 ",color:"red"}},{{text:"Red"}}],[" ",{{score:{{name:"#red",objective:"{ns}.mp.team"}},color:"white"}}]]'
	sb_blue = f'[[{{text:" 🔵 ",color:"blue"}},{{text:"Blue"}}],[" ",{{score:{{name:"#blue",objective:"{ns}.mp.team"}},color:"white"}}]]'
	sb_limit = f'[{{text:" First to ",color:"gray"}},{{score:{{name:"#score_limit",objective:"{ns}.data"}},color:"white"}}]'
	sb_spacer = '" "'

	## Team sidebar (TDM/SND) — takes $(title) macro arg
	write_versioned_function("multiplayer/create_sidebar_team", f"""
scoreboard objectives remove {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"$(title)",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	## FFA sidebar — ranked players with kills using bs.sidebar
	write_versioned_function("multiplayer/create_sidebar_ffa", f"""
function {ns}:v{version}/multiplayer/refresh_sidebar_ffa
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	# FFA sidebar refresh: ranks players by kills, builds sidebar with top 10
	# Called every second from timer_display and on kills
	ffa_rank_code = f"""
# Initialize sidebar header in storage
data modify storage {ns}:temp ffa_sb set value [{sb_timer},{sb_spacer},{sb_limit},{sb_spacer}]

# Reset ranks and tag candidates
scoreboard players set @a {ns}.mp.ffa_rank 0
tag @a[scores={{{ns}.mp.in_game=1..}}] add {ns}.ffa_candidate
"""
	for i in range(1, 11):
		ffa_rank_code += f"""
# Rank {i}
execute unless entity @a[tag={ns}.ffa_candidate] run return run function {ns}:v{version}/multiplayer/build_sidebar_ffa with storage {ns}:temp
scoreboard players set #ffa_max {ns}.data -1
execute as @a[tag={ns}.ffa_candidate] run scoreboard players operation #ffa_max {ns}.data > @s {ns}.mp.kills
tag @a remove {ns}.ffa_top
execute as @a[tag={ns}.ffa_candidate] if score @s {ns}.mp.kills = #ffa_max {ns}.data run tag @s add {ns}.ffa_top
execute as @p[tag={ns}.ffa_top,sort=arbitrary] run scoreboard players set @s {ns}.mp.ffa_rank {i}
tag @a[tag={ns}.ffa_top] remove {ns}.ffa_top
execute as @a[scores={{{ns}.mp.ffa_rank={i}}}] run tag @s remove {ns}.ffa_candidate
data modify storage {ns}:temp ffa_sb append value [[{{text:" {i}. ",color:"gold"}},{{selector:"@a[scores={{{ns}.mp.ffa_rank={i}}}]",color:"yellow"}}],{{score:{{name:"@a[scores={{{ns}.mp.ffa_rank={i}}}]",objective:"{ns}.mp.kills"}},color:"white"}}]
"""
	ffa_rank_code += f"""
# Build
function {ns}:v{version}/multiplayer/build_sidebar_ffa with storage {ns}:temp
"""
	write_versioned_function("multiplayer/refresh_sidebar_ffa", ffa_rank_code)

	## FFA sidebar build (macro function)
	write_versioned_function("multiplayer/build_sidebar_ffa", f"""
tag @a remove {ns}.ffa_candidate
scoreboard objectives remove {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Free For All",color:"gold",bold:true}},contents:$(ffa_sb)}}
""")

	## Domination sidebar — shows team scores + point ownership per zone
	# Point status display helper (0=⚪, 1=🔴, 2=🔵) — updated each tick via refresh
	# We build DOM point lines that reference #dom_owner_X scores
	# Since sidebar can't do conditionals, we use a helper function to rebuild sidebar each score_tick
	write_versioned_function("multiplayer/create_sidebar_dom", f"""
function {ns}:v{version}/multiplayer/refresh_sidebar_dom
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	# DOM sidebar refresh: rebuilds the sidebar content with current point ownership
	# Called every score_tick (every 5 seconds) and on point captures
	write_versioned_function("multiplayer/refresh_sidebar_dom", f"""
# Build point status strings based on ownership scores
# Zone A
execute if score #dom_owner_a {ns}.data matches 0 run data modify storage {ns}:temp dom_sb.a set value '[" ",{{"text":"A: ⚪ Neutral","color":"gray"}}]'
execute if score #dom_owner_a {ns}.data matches 1 run data modify storage {ns}:temp dom_sb.a set value '[" ",{{"text":"A: 🔴 Red","color":"red"}}]'
execute if score #dom_owner_a {ns}.data matches 2 run data modify storage {ns}:temp dom_sb.a set value '[" ",{{"text":"A: 🔵 Blue","color":"blue"}}]'

# Zone B
execute if score #dom_owner_b {ns}.data matches 0 run data modify storage {ns}:temp dom_sb.b set value '[" ",{{"text":"B: ⚪ Neutral","color":"gray"}}]'
execute if score #dom_owner_b {ns}.data matches 1 run data modify storage {ns}:temp dom_sb.b set value '[" ",{{"text":"B: 🔴 Red","color":"red"}}]'
execute if score #dom_owner_b {ns}.data matches 2 run data modify storage {ns}:temp dom_sb.b set value '[" ",{{"text":"B: 🔵 Blue","color":"blue"}}]'

# Zone C
execute if score #dom_owner_c {ns}.data matches 0 run data modify storage {ns}:temp dom_sb.c set value '[" ",{{"text":"C: ⚪ Neutral","color":"gray"}}]'
execute if score #dom_owner_c {ns}.data matches 1 run data modify storage {ns}:temp dom_sb.c set value '[" ",{{"text":"C: 🔴 Red","color":"red"}}]'
execute if score #dom_owner_c {ns}.data matches 2 run data modify storage {ns}:temp dom_sb.c set value '[" ",{{"text":"C: 🔵 Blue","color":"blue"}}]'

# Build sidebar with dynamic point entries
function {ns}:v{version}/multiplayer/build_sidebar_dom with storage {ns}:temp dom_sb
""")

	write_versioned_function("multiplayer/build_sidebar_dom", f"""
scoreboard objectives remove {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Domination",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},$(a),$(b),$(c),{sb_spacer},{sb_limit}]}}
""")

	## Hardpoint sidebar — shows team scores + controlling team + time to move
	write_versioned_function("multiplayer/create_sidebar_hp", f"""
scoreboard objectives remove {ns}.sidebar
function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Hardpoint",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},[{{text:" Zone: ",color:"dark_purple"}},{{score:{{name:"#hp_rotate_sec",objective:"{ns}.data"}},color:"white"}},{{text:"s left",color:"gray"}}],{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	# Shooting Block During Prep ────────────────────────────────

	## Prepend to right_click: block shooting during prep phase
	write_versioned_function("player/right_click", f"""
# Block shooting during multiplayer prep phase
execute if score @s {ns}.mp.in_game matches 1 if data storage {ns}:multiplayer game{{state:"preparing"}} run return run scoreboard players set @s {ns}.pending_clicks 0
""", prepend=True)

	# Prep Phase ────────────────────────────────────────────────

	## Prep tick: during 10s warmup, detect class changes and apply immediately
	write_versioned_function("multiplayer/prep_tick", f"""
# Check for class changes and apply immediately
execute as @a[scores={{{ns}.mp.in_game=1}}] unless score @s {ns}.mp.class = @s {ns}.mp.prev_class unless score @s {ns}.mp.class matches 0 at @s run function {ns}:v{version}/multiplayer/apply_class
execute as @a[scores={{{ns}.mp.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class
""")

	## End prep: unfreeze players, transition to active
	write_versioned_function("multiplayer/end_prep", f"""
# Only if still preparing (game might have been stopped)
execute unless data storage {ns}:multiplayer game{{state:"preparing"}} run return fail

# Restore movement
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:jump_strength base set 0.42
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:waypoint_receive_range base set 0.0

# Clear prep effects
effect clear @a[scores={{{ns}.mp.in_game=1}}] darkness
effect clear @a[scores={{{ns}.mp.in_game=1}}] blindness
effect clear @a[scores={{{ns}.mp.in_game=1}}] night_vision

# Re-apply permanent saturation for the active game
effect give @a[scores={{{ns}.mp.in_game=1}}] saturation infinite 255 true

# Set state to active
data modify storage {ns}:multiplayer game.state set value "active"

# Announce
tellraw @a [{{"text":"","color":"green","bold":true}},"⚔ ",{{"text":"GO! GO! GO!"}}]
""")

