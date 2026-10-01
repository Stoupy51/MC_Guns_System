""" The game tick, the Tracker perk, the match timer and boundary enforcement. """
# Imports
from stewbeet import Mem, write_tick_file, write_versioned_function

from ...core.respawn_countdown import respawn_countdown_tick_lines
from ...core.weapon_drop import WeaponDrop
from ...helpers import MGS_TAG
from ...helpers.probes import Probe
from ..gamemodes.dispatch import gm_dispatch


# Functions
def write_multiplayer_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_tick_file(f"""
execute if data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/game_tick
execute if data storage {ns}:multiplayer game{{state:"preparing"}} run function {ns}:v{version}/multiplayer/prep_tick
""")

	write_versioned_function("multiplayer/game_tick", f"""
# The XP bar is the progression HUD, so a stray orb would show a level nobody earned; tick_player re-asserts the bar every second.
kill @e[type=experience_orb]

{respawn_countdown_tick_lines(ns, "mp", f"{ns}:v{version}/multiplayer/actual_respawn")}

{WeaponDrop.weapon_drop_tick_lines(ns)}

# Real time through #tick_delta, unless the gamemode claimed #mp_timer in its setup: round-based modes drive it from their own clock
# (S&D round timer then fuse, Demolition plant-aware clock), since a match-wide limit cannot judge a best-of-N format.
execute if score #mp_mode_owns_timer {ns}.data matches 0 run scoreboard players operation #mp_timer {ns}.data -= #tick_delta {ns}.data

# Keyed to #total_tick: under lag #tick_delta can jump past a `#mp_timer % 20` hit.
execute store result score #tick_mod {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #tick_mod {ns}.data %= #20 {ns}.data
execute if score #tick_mod {ns}.data matches 0 run function {ns}:v{version}/multiplayer/timer_display

# Never for a mode that owns the score, where 0 is a round event it handles.
execute if score #mp_mode_owns_timer {ns}.data matches 0 if score #mp_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/time_up

# See multiplayer/enforce_bounds.
execute store result score #bounds_phase {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #bounds_phase {ns}.data %= #4 {ns}.data

# Bounds and OOB markers in one scan, skipping respawn-protected and non-playing players.
execute as @e[type=player,scores={{{ns}.mp.in_game=1,{ns}.mp.death_count=0}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/multiplayer/enforce_bounds

{gm_dispatch(ns, version, "tick")}

# Tracker perk: enemy footprints every 6 ticks.
execute store result score #tick_mod {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #tick_mod {ns}.data %= #6 {ns}.data
execute if score #tick_mod {ns}.data matches 0 if entity @a[scores={{{ns}.mp.in_game=1,{ns}.special.tracker=1..}}] run function {ns}:v{version}/multiplayer/perks/tracker_tick

function {ns}:v{version}/shared/maps/call_script_at_base {{script:"tick"}}
""")

	## One pass over the live players: a footprint at each one's feet.
	write_versioned_function("multiplayer/perks/tracker_tick", f"""
execute as @a[scores={{{ns}.mp.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/multiplayer/perks/tracker_footprint
""")

	## Run as the tracked player, at them: the footprint shows to enemy Tracker holders only
	## (team modes: the other team; FFA: every other holder, the player excluded by distance).
	write_versioned_function("multiplayer/perks/tracker_footprint", f"""
execute if score @s {ns}.mp.team matches 1 run particle minecraft:dust{{color:[0.95,0.85,0.2],scale:0.8}} ~ ~0.1 ~ 0.15 0.02 0.15 0 3 force @a[scores={{{ns}.special.tracker=1..,{ns}.mp.team=2}}]
execute if score @s {ns}.mp.team matches 2 run particle minecraft:dust{{color:[0.95,0.85,0.2],scale:0.8}} ~ ~0.1 ~ 0.15 0.02 0.15 0 3 force @a[scores={{{ns}.special.tracker=1..,{ns}.mp.team=1}}]
execute if score @s {ns}.mp.team matches 0 run particle minecraft:dust{{color:[0.95,0.85,0.2],scale:0.8}} ~ ~0.1 ~ 0.15 0.02 0.15 0 3 force @a[scores={{{ns}.special.tracker=1..}},distance=0.1..]
""")

	## Actionbar timer (minutes:seconds).
	write_versioned_function("multiplayer/timer_display", f"""
execute store result score #timer_sec {ns}.data run scoreboard players get #mp_timer {ns}.data
scoreboard players operation #timer_sec {ns}.data /= #20 {ns}.data
execute store result score #timer_min {ns}.data run scoreboard players get #timer_sec {ns}.data
scoreboard players operation #timer_min {ns}.data /= #60 {ns}.data
scoreboard players operation #timer_mod {ns}.data = #timer_sec {ns}.data
scoreboard players operation #timer_mod {ns}.data %= #60 {ns}.data

# Zero-padded seconds for the sidebar.
scoreboard players operation #timer_tens {ns}.data = #timer_mod {ns}.data
scoreboard players operation #timer_tens {ns}.data /= #10 {ns}.data
scoreboard players operation #timer_ones {ns}.data = #timer_mod {ns}.data
scoreboard players operation #timer_ones {ns}.data %= #10 {ns}.data

execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function #bs.sidebar:refresh {{objective:"{ns}.sidebar"}}
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/refresh_sidebar_ffa
""")

	write_versioned_function("multiplayer/time_up", f"""
# FFA: most kills wins.
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/ffa_time_up

# Team modes: most points wins.
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} if score #red {ns}.mp.team > #blue {ns}.mp.team run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} if score #blue {ns}.mp.team > #red {ns}.mp.team run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} if score #red {ns}.mp.team = #blue {ns}.mp.team run function {ns}:v{version}/multiplayer/game_draw
""")

	write_versioned_function("multiplayer/ffa_time_up", f"""
tellraw @a [{MGS_TAG},{{"text":"Time's up!","color":"gold"}}]

scoreboard players set #max_kills {ns}.data 0
scoreboard players operation #max_kills {ns}.data > @a[scores={{{ns}.mp.in_game=1}}] {ns}.mp.kills

execute as @a[scores={{{ns}.mp.in_game=1}}] if score @s {ns}.mp.kills = #max_kills {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/ffa/player_wins
""")

	write_versioned_function("multiplayer/game_draw", f"""
tellraw @a ["","🤝 ",{{"text":"Draw!","color":"gold","bold":true}}]
function {ns}:v{version}/multiplayer/stop
""")

	## Run as each in-game player, at them.
	write_versioned_function("multiplayer/check_bounds", f"""
{Probe.pos()}
execute store result score @s {ns}.mp.bx run data get storage {ns}:temp _probe_pos[0]
execute store result score @s {ns}.mp.by run data get storage {ns}:temp _probe_pos[1]
execute store result score @s {ns}.mp.bz run data get storage {ns}:temp _probe_pos[2]

# Any axis out of range is out of bounds.
execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
""")

	## Run as a playing player, from the one scan in game_tick.
	write_versioned_function("multiplayer/enforce_bounds", f"""
# Only when the map defines a boundary box; may turn @s into a spectator.
execute unless score @s {ns}.mp.bphase matches 0..3 run function {ns}:v{version}/multiplayer/assign_bphase
execute if score #mp_has_boundary {ns}.data matches 1 if score @s {ns}.mp.bphase = #bounds_phase {ns}.data run function {ns}:v{version}/multiplayer/check_bounds

# Skipped if the coordinate check just eliminated @s, or the death would count twice.
execute if entity @s[gamemode=!spectator] if entity @e[tag={ns}.oob_point,distance=..5] run function {ns}:v{version}/multiplayer/bounds_kill
""")

	## Round-robin over the 4 phases; the score persists, so only players leaving mid-game can unbalance them.
	write_versioned_function("multiplayer/assign_bphase", f"""
scoreboard players operation @s {ns}.mp.bphase = #bphase_next {ns}.data
scoreboard players add #bphase_next {ns}.data 1
scoreboard players operation #bphase_next {ns}.data %= #4 {ns}.data
""")

	## Out of bounds or near an OOB marker: a simulated death, never /kill.
	write_versioned_function("multiplayer/bounds_kill", f"""
# No attacker: an environmental death.
data modify storage {ns}:input with set value {{}}
function {ns}:v{version}/multiplayer/simulate_death
""")

