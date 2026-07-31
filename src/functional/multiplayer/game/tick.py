""" The game tick, the Tracker perk, the match timer and boundary enforcement. """
# Imports
from stewbeet import Mem, write_tick_file, write_versioned_function

from ...core.respawn_countdown import respawn_countdown_tick_lines
from ...core.weapon_drop import WeaponDrop
from ...helpers import MGS_TAG
from ..gamemodes.dispatch import gm_dispatch


# Functions
def write_multiplayer_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Game Tick (runs once per server tick when game is active)
	write_tick_file(f"""
# Multiplayer game tick
execute if data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/game_tick
execute if data storage {ns}:multiplayer game{{state:"preparing"}} run function {ns}:v{version}/multiplayer/prep_tick
""")

	write_versioned_function("multiplayer/game_tick", f"""
{respawn_countdown_tick_lines(ns, "mp", f"{ns}:v{version}/multiplayer/actual_respawn")}

{WeaponDrop.weapon_drop_tick_lines(ns)}

# Timer (real-time via #tick_delta), unless the gamemode claimed #mp_timer for itself in its setup.
# Round-based modes drive that score from their own clock so the HUD shows what actually decides something
# (S&D: the round timer then the bomb fuse — Demolition: a clock that stops on a plant and grows on a
# destroy), and a match-wide time limit cannot arbitrate a best-of-N format anyway. A claim flag rather
# than a list of gamemode names here: the list was going to grow once per round-based mode.
execute if score #mp_mode_owns_timer {ns}.data matches 0 run scoreboard players operation #mp_timer {ns}.data -= #tick_delta {ns}.data

# Timer display every second (20 ticks; keyed to #total_tick — a #mp_timer %20 hit can be
# skipped entirely when #tick_delta jumps by 2+ under lag)
execute store result score #tick_mod {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #tick_mod {ns}.data %= #20 {ns}.data
execute if score #tick_mod {ns}.data matches 0 run function {ns}:v{version}/multiplayer/timer_display

# Time's up — never for a mode that owns the score, where reaching 0 is a ROUND event it handles itself
execute if score #mp_mode_owns_timer {ns}.data matches 0 if score #mp_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/time_up

# Which boundary-check phase runs this tick (see multiplayer/enforce_bounds)
execute store result score #bounds_phase {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #bounds_phase {ns}.data %= #4 {ns}.data

# Boundary + out-of-bounds enforcement in ONE pass over the playing-players selector (was two
# scans over the identical, multi-filter selector). Skips respawn-protected/non-playing players.
execute as @e[type=player,scores={{{ns}.mp.in_game=1,{ns}.mp.death_count=0}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/multiplayer/enforce_bounds

# Gamemode tick dispatch
{gm_dispatch(ns, version, "tick")}

# Tracker perk: render enemy footprints to perked players (every 6 ticks)
execute store result score #tick_mod {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #tick_mod {ns}.data %= #6 {ns}.data
execute if score #tick_mod {ns}.data matches 0 if entity @a[scores={{{ns}.mp.in_game=1,{ns}.special.tracker=1..}}] run function {ns}:v{version}/multiplayer/perks/tracker_tick

# Call map-defined tick script
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"tick"}}
""")

	## perks/tracker_tick - One pass over all live players: drop a footprint at each one's feet
	write_versioned_function("multiplayer/perks/tracker_tick", f"""
execute as @a[scores={{{ns}.mp.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/multiplayer/perks/tracker_footprint
""")

	## perks/tracker_footprint - @s = the tracked player (at their position); the footprint is forced to enemy Tracker holders only, via a single team-filtered selector.
	## (Team modes: opposite team.
	## FFA/team 0: every other Tracker holder, excluded via distance.)
	write_versioned_function("multiplayer/perks/tracker_footprint", f"""
execute if score @s {ns}.mp.team matches 1 run particle minecraft:dust{{color:[0.95,0.85,0.2],scale:0.8}} ~ ~0.1 ~ 0.15 0.02 0.15 0 3 force @a[scores={{{ns}.special.tracker=1..,{ns}.mp.team=2}}]
execute if score @s {ns}.mp.team matches 2 run particle minecraft:dust{{color:[0.95,0.85,0.2],scale:0.8}} ~ ~0.1 ~ 0.15 0.02 0.15 0 3 force @a[scores={{{ns}.special.tracker=1..,{ns}.mp.team=1}}]
execute if score @s {ns}.mp.team matches 0 run particle minecraft:dust{{color:[0.95,0.85,0.2],scale:0.8}} ~ ~0.1 ~ 0.15 0.02 0.15 0 3 force @a[scores={{{ns}.special.tracker=1..}},distance=0.1..]
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
tellraw @a ["","🤝 ",{{"text":"Draw!","color":"gold","bold":true}}]
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

	## Per-player boundary + OOB enforcement (one scan in game_tick dispatches this).
	## @s = a playing player.
	## Merges the former two separate game_tick passes over the same selector.
	write_versioned_function("multiplayer/enforce_bounds", f"""
# Coordinate bounds (only when the map defines a boundary box). May eliminate @s -> spectator.
execute unless score @s {ns}.mp.bphase matches 0..3 run function {ns}:v{version}/multiplayer/assign_bphase
execute if score #mp_has_boundary {ns}.data matches 1 if score @s {ns}.mp.bphase = #bounds_phase {ns}.data run function {ns}:v{version}/multiplayer/check_bounds

# OOB markers. Skip if the coordinate check just eliminated @s this tick (now a spectator) — the
# original two-pass form excluded such players via its gamemode=!spectator selector, so doing the
# OOB kill here too would double-count the death.
execute if entity @s[gamemode=!spectator] if entity @e[tag={ns}.oob_point,distance=..5] run function {ns}:v{version}/multiplayer/bounds_kill
""")

	## Give @s the next boundary-check phase, round-robin so the 4 phases stay evenly filled.
	## Runs once per player (the score persists), so an uneven split can only come from players leaving mid-game, which at worst unbalances a handful of position reads per tick.
	write_versioned_function("multiplayer/assign_bphase", f"""
scoreboard players operation @s {ns}.mp.bphase = #bphase_next {ns}.data
scoreboard players add #bphase_next {ns}.data 1
scoreboard players operation #bphase_next {ns}.data %= #4 {ns}.data
""")

	## Environmental kill: out of boundaries or near an OOB marker (simulate death, never /kill)
	write_versioned_function("multiplayer/bounds_kill", f"""
# Clear attacker input (environmental death) and simulate death
data modify storage {ns}:input with set value {{}}
function {ns}:v{version}/multiplayer/simulate_death
""")

