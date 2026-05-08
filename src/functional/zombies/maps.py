
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG


def generate_zombies_maps() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# ── Kino der Toten ──────────────────────────────────────────────────────────
	# Map registration: placeholder data (base_coordinates and spawn arrays TBD)
	write_versioned_function("maps/zombies/kino_der_toten/register", f"""
# Kino der Toten map registration
execute unless data storage {ns}:maps zombies[{{id:"kino_der_toten"}}] run data modify storage {ns}:maps zombies append value {{id:"kino_der_toten", name:"Kino der Toten", description:"Black Ops 1 | Classic Zombies", base_coordinates:[0,0,0], spawning_points:{{zombies:[],players:[]}}, out_of_bounds:[], boundaries:[]}}
""", tags=[f"{ns}:zombies/register_maps"])  # noqa: E501

	# Calls functions — guard then delegate, registered to the shared function tags
	_guard = (
		f'execute if data storage {ns}:zombies game{{state:"active"}}'
		f' if data storage {ns}:zombies game{{map_id:"kino_der_toten"}}'
	)
	for script in ["start", "tick", "join", "leave", "respawn", "power"]:
		write_versioned_function(f"maps/zombies/kino_der_toten/calls/{script}",
			f"{_guard} run return run function {ns}:v{version}/maps/zombies/kino_der_toten/{script}",
			tags=[f"{ns}:maps/{script}_script"]
		)

	# Logic functions (actual work)
	write_versioned_function("maps/zombies/kino_der_toten/start", f"""
# Kino der Toten map start script
# Called once when zombies game transitions to active
# @within  #{ns}:maps/start_script (via calls/start)

# Initialize kino-specific data scores
scoreboard players set #kino_tp_state {ns}.data 0
scoreboard players set #kino_tp_timer {ns}.data 0
scoreboard players set #kino_tp_cd {ns}.data 0
scoreboard players set #kino_met_count {ns}.data 0

# Set the lobby to theater door closed
execute positioned ~-19 ~0 ~-1 run fill ~ ~ ~ ~2 ~2 ~ cobblestone

# Summon all interactions
## Teleporter
execute positioned ~-57 ~-1 ~9 run summon interaction ~ ~ ~ {{Tags:["{ns}.kino","{ns}.kino.teleporter_theater","bs.entity.interaction"],width:1.0f,height:2.0f}}
execute positioned ~ ~ ~ run summon interaction ~ ~ ~ {{Tags:["{ns}.kino","{ns}.kino.teleporter_lobby","bs.entity.interaction"],width:1.0f,height:1.0f}}

## Meteorites
execute positioned ~-12 ~0 ~-5 run summon interaction ~ ~ ~ {{Tags:["{ns}.kino","{ns}.kino.meteorite_1","bs.entity.interaction"],width:1.1f,height:2.0f}}
execute positioned ~-58 ~-2 ~-22 run summon interaction ~ ~ ~ {{Tags:["{ns}.kino","{ns}.kino.meteorite_2","bs.entity.interaction"],width:1.1f,height:2.0f}}
execute positioned ~-54 ~4 ~39 run summon interaction ~ ~ ~ {{Tags:["{ns}.kino","{ns}.kino.meteorite_3","bs.entity.interaction"],width:1.1f,height:2.0f}}

# Register right-click events for all kino interactions (target = interaction entity itself)
execute as @e[tag={ns}.kino] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/maps/zombies/kino_der_toten/on_right_click",executor:"target"}}
""")

	# ── tick ──────────────────────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/tick", f"""
# Kino der Toten map tick (runs every game tick while active)
# @within  #{ns}:maps/tick_script (via calls/tick)

function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/tick
""")

	# ── join ──────────────────────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/join", f"""
# Kino der Toten map join script
# @s = joining player
# @within  #{ns}:maps/join_script (via calls/join)
""")

	# ── leave ─────────────────────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/leave", f"""
# Kino der Toten map leave script (game ended / cleanup)
# @within  #{ns}:maps/leave_script (via calls/leave)

# Kill all kino interaction entities
kill @e[tag={ns}.kino]

# Remove in-teleporter tag from all players
tag @a remove {ns}.kino.in_tp

# Reset kino data scores
scoreboard players set #kino_tp_state {ns}.data 0
scoreboard players set #kino_tp_timer {ns}.data 0
scoreboard players set #kino_tp_cd {ns}.data 0
scoreboard players set #kino_met_count {ns}.data 0
""")

	# ── respawn ───────────────────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/respawn", """
# Kino der Toten map respawn script
# @s = respawning player
# @within  #mgs:maps/respawn_script (via calls/respawn)
""")

	# ── on_right_click ────────────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/on_right_click", f"""
# Route right-click to the correct sub-handler based on which entity was clicked
# @s = interaction entity itself; use 'execute on target' to reach the clicking player
execute if entity @s[tag={ns}.kino.teleporter_theater] run return run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/on_theater_click
execute if entity @s[tag={ns}.kino.teleporter_lobby] run return run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/on_lobby_click
execute if entity @s[tag={ns}.kino.meteorite_1] run return run function {ns}:v{version}/maps/zombies/kino_der_toten/meteorite/on_click
execute if entity @s[tag={ns}.kino.meteorite_2] run return run function {ns}:v{version}/maps/zombies/kino_der_toten/meteorite/on_click
execute if entity @s[tag={ns}.kino.meteorite_3] run return run function {ns}:v{version}/maps/zombies/kino_der_toten/meteorite/on_click
""")

	# ── teleporter/on_theater_click ────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/on_theater_click", f"""
# State 0 (idle): start linking — player must now click the lobby pad
execute if score #kino_tp_state {ns}.data matches 0 run return run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/start_link
# State 2 (armed): lobby was linked, execute the actual teleport
execute if score #kino_tp_state {ns}.data matches 2 at @s run return run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/activate
# Any other state (linking/active/returning/cooldown): deny
function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/deny_recharging
""")

	# ── teleporter/start_link ───────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/start_link", f"""
# State 1: theater clicked — waiting for the lobby pad to be clicked
scoreboard players set #kino_tp_state {ns}.data 1
playsound minecraft:block.beacon.power_select block @a[distance=..50] ~ ~ ~ 1 1
""")

	# ── teleporter/on_lobby_click ─────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/on_lobby_click", f"""
# Only arm when we are in the linking state
execute unless score #kino_tp_state {ns}.data matches 1 run return fail

# State 2: armed — clicking theater again will now trigger the teleport
scoreboard players set #kino_tp_state {ns}.data 2
playsound minecraft:block.beacon.activate block @a[distance=..50] ~ ~ ~ 1 1
""")

	# ── teleporter/activate ───────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/activate", f"""
# @s = theater interaction entity (armed, state 2)
# Tag all nearby in-game players (within 3 blocks)
tag @a[distance=..3,scores={{{ns}.zb.in_game=1}},gamemode=!spectator] add {ns}.kino.in_tp

# Teleport tagged players to the projection room
execute positioned ~57 ~1 ~-9 run tp @a[tag={ns}.kino.in_tp] ~-22 ~6 ~0

# State 3: players in projection room, 600t (30s) countdown
scoreboard players set #kino_tp_state {ns}.data 3
scoreboard players set #kino_tp_timer {ns}.data 600
""")

	write_versioned_function("maps/zombies/kino_der_toten/teleporter/deny_recharging", f"""
# @s = interaction entity; reach the player via 'on target'
execute on target run tellraw @s [{MGS_TAG},{{"text":"The teleporter is recharging...","color":"yellow"}}]
execute on target at @s run function {ns}:v{version}/zombies/feedback/sound_deny
""")

	# ── teleporter/tick ───────────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/tick", f"""
# State 3: players in projection room — count down, then scatter to random lobby spots
execute if score #kino_tp_state {ns}.data matches 3 run scoreboard players remove #kino_tp_timer {ns}.data 1
execute if score #kino_tp_state {ns}.data matches 3 if score #kino_tp_timer {ns}.data matches ..0 run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/return_players

# State 4: players at random spots — count down 5s (100t), then tp all to lobby
execute if score #kino_tp_state {ns}.data matches 4 run scoreboard players remove #kino_tp_timer {ns}.data 1
execute if score #kino_tp_state {ns}.data matches 4 if score #kino_tp_timer {ns}.data matches ..0 run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/return_to_lobby

# State 5: cooldown — count down, then reset to idle (state 0)
execute if score #kino_tp_state {ns}.data matches 5 run scoreboard players remove #kino_tp_cd {ns}.data 1
execute if score #kino_tp_state {ns}.data matches 5 if score #kino_tp_cd {ns}.data matches ..0 run scoreboard players set #kino_tp_state {ns}.data 0
""")

	# ── teleporter/return_players ─────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/return_players", f"""
# Scatter each tagged player to a random lobby position
execute as @a[tag={ns}.kino.in_tp] run function {ns}:v{version}/maps/zombies/kino_der_toten/teleporter/return_one
# Keep kino.in_tp tags — needed by return_to_lobby after 5 seconds

# State 4: 5 seconds (100t) before teleporting everyone back to the lobby pad
scoreboard players set #kino_tp_state {ns}.data 4
scoreboard players set #kino_tp_timer {ns}.data 100
""")

	# ── teleporter/return_to_lobby ─────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/return_to_lobby", f"""
# Teleport all returning players to the lobby teleporter pad position
execute as @a[tag={ns}.kino.in_tp] at @e[tag={ns}.kino.teleporter_lobby] run tp @s ~ ~ ~

# Clean up tags
tag @a remove {ns}.kino.in_tp

# State 5: enter cooldown (3600t = 3 min)
scoreboard players set #kino_tp_state {ns}.data 5
scoreboard players set #kino_tp_cd {ns}.data 3600
""")

	# ── teleporter/return_one ─────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/teleporter/return_one", f"""
# @s = player returning from theater — pick a random lobby spot
execute store result score #tp_random {ns}.data run random value 1..5
execute if score #tp_random {ns}.data matches 1 run tp @s ~9 ~-4 ~-40
execute if score #tp_random {ns}.data matches 2 run tp @s ~-34 ~4 ~54
execute if score #tp_random {ns}.data matches 3 run tp @s ~-27 ~4 ~-82
execute if score #tp_random {ns}.data matches 4 run tp @s ~-97 ~7 ~13
execute if score #tp_random {ns}.data matches 5 run tp @s ~40 ~4 ~39
""")

	# ── meteorite/on_click ────────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/meteorite/on_click", f"""
# @s = interaction entity itself
# Guard: this meteorite is already activated
execute if entity @s[tag={ns}.kino.met_active] run return fail

# Mark meteorite as activated and increment counter
tag @s add {ns}.kino.met_active
scoreboard players add #kino_met_count {ns}.data 1

# On third meteorite: play the 115 song
execute if score #kino_met_count {ns}.data matches 3 run function {ns}:v{version}/maps/zombies/kino_der_toten/meteorite/play_song
""")

	# ── meteorite/play_song ───────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/meteorite/play_song", f"""
# Play 115 for all in-game players at their own position
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/music/115_song record @s ~ ~ ~ 0.5 1
""")

	# ── power ─────────────────────────────────────────────────────────────────
	write_versioned_function("maps/zombies/kino_der_toten/power", f"""
# Kino der Toten power-on script
# Called once when the power switch is activated
# @within  #{ns}:maps/on_power (via calls/power)

# Open the lobby-to-theater door
execute positioned ~-19 ~0 ~-1 run fill ~ ~ ~ ~2 ~2 ~ air
""")

