""" Starting a mission: map preload, the prep phase and spawning every enemy. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG, FunctionalHelpers


# Functions
def write_missions_start() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Game Start
	write_versioned_function("missions/start", f"""
# Prevent starting if already active or preparing
{FunctionalHelpers.game_start_guards(ns, "missions", "Mission")}

# Require at least one opted-in player (players are independent until added via Manage Players / + Join)
execute unless entity @a[scores={{{ns}.mi.in_game=1}}] run return run tellraw @s [{MGS_TAG},{{"text":"No players have joined the mission — use Manage Players first.","color":"red"}}]

{FunctionalHelpers.mode_start_map_bootstrap_lines(ns, "missions", True)}

# Blue team for missions
team add {ns}.blue
team modify {ns}.blue color blue
team modify {ns}.blue friendlyFire false
team modify {ns}.blue nametagVisibility hideForOtherTeams

# Mission mob team (created once)
team add {ns}.mi_mobs
team modify {ns}.mi_mobs color dark_red
team modify {ns}.mi_mobs friendlyFire true

# Reset scores (in_game is left untouched: it's the opt-in flag, set via Manage Players / + Join)
scoreboard players set #mi_timer {ns}.data 0
scoreboard players set #mi_total_enemies {ns}.data 0
scoreboard players set #mi_has_boundary {ns}.data 0
scoreboard players set @a {ns}.mi.kills 0
scoreboard players set @a {ns}.mi.deaths 0
scoreboard players set @a {ns}.mp.spectate_timer 0

# The deathCount criterion keeps counting outside of games, so a death taken back in the lobby would
# still be sitting on the score when the state flips to active — player/tick would then fire
# missions/on_respawn immediately, killing everyone for real the instant the prep countdown ends.
# Multiplayer and zombies clear it at start for the same reason.
scoreboard players set @a {ns}.mp.death_count 0

# Missions are fully cooperative: all opted-in players join the blue team
scoreboard players set @a[scores={{{ns}.mi.in_game=1}}] {ns}.mp.team 1
team join {ns}.blue @a[scores={{{ns}.mi.in_game=1}}]

# Enable class menu for mission players
tag @a[scores={{{ns}.mi.in_game=1}}] add {ns}.give_class_menu

# Snapshot player total kills at mission start for per-mission kill delta
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mi.kill_base = @s {ns}.mi.kill_total

# Set gamerules
gamemode spectator @a[scores={{{ns}.mi.in_game=1}}]
gamerule immediate_respawn true
gamerule keep_inventory true

{FunctionalHelpers.regen_enable_lines(ns)}

# Store base coordinates for offset
function {ns}:v{version}/shared/load_base_coordinates {{mode:"missions"}}

# Detect whether this map defines a boundary (needs 2 points)
execute if data storage {ns}:missions game.map.boundaries[0] if data storage {ns}:missions game.map.boundaries[1] run scoreboard players set #mi_has_boundary {ns}.data 1

# Normalize and store boundaries only when they exist
execute if score #mi_has_boundary {ns}.data matches 1 run function {ns}:v{version}/shared/load_bounds {{mode:"missions"}}

# Forceload the mission area to ensure chunks are loaded
execute if score #mi_has_boundary {ns}.data matches 1 run function {ns}:v{version}/shared/forceload_area

# Teleport all players as spectator to base coordinates for chunk preloading
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #gm_base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #gm_base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #gm_base_z {ns}.data
execute as @a[scores={{{ns}.mi.in_game=1}}] run function {ns}:v{version}/shared/tp_to_position with storage {ns}:temp _tp

# Schedule preload completion after 1 second
{FunctionalHelpers.schedule_preload_complete_line(ns, "missions")}

# Announce
tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"Loading mission area...","color":"yellow"}}]
""")

	## Preload complete → transition to prep phase
	write_versioned_function("missions/preload_complete", f"""
# Guard: only if still preparing
execute unless data storage {ns}:missions game{{state:"preparing"}} run return fail

# Switch to adventure mode
gamemode adventure @a[scores={{{ns}.mi.in_game=1}}]

# Summon OOB markers
function {ns}:v{version}/shared/summon_oob {{mode:"missions"}}

# Summon spawn point markers
function {ns}:v{version}/missions/summon_spawns

# Signal mission start
function #{ns}:missions/on_mission_start

# Teleport all players to mission spawns
function {ns}:v{version}/missions/tp_all_to_spawns

# Freeze players during prep
{FunctionalHelpers.prep_freeze_lines(ns, "mi")}
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:waypoint_receive_range base reset

# Give loadout to players who already have a class
execute as @a[scores={{{ns}.mi.in_game=1}}] at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# Auto-apply default custom loadout if no class set
# (add 0 initializes unset scores so the 'matches 0' check below can succeed)
scoreboard players add @a {ns}.mp.class 0
execute as @a[scores={{{ns}.mi.in_game=1}}] at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default

# Show class selection
execute as @a[scores={{{ns}.mi.in_game=1}}] run function {ns}:v{version}/multiplayer/select_class

# Store current class for change detection
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class

# Schedule end of prep (9 seconds remaining)
schedule function {ns}:v{version}/missions/end_prep 180t

# Announce
tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"Preparing! Choose your class! Mission starts in 9 seconds!","color":"yellow"}}]
""")

	## Prep Tick (check for class changes during preparation)
	write_versioned_function("missions/prep_tick", f"""
# Detect class changes during prep
execute as @a[scores={{{ns}.mi.in_game=1}}] unless score @s {ns}.mp.prev_class = @s {ns}.mp.class at @s run function {ns}:v{version}/multiplayer/apply_class
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class
""")

	## End Prep → Start Mission (spawn all enemies)
	write_versioned_function("missions/end_prep", f"""
{FunctionalHelpers.end_prep_transition_lines(ns, "missions", "mi")}

# Spawn all enemies from map data
function {ns}:v{version}/missions/spawn_all_enemies

# A mission with no enemies would instantly "complete" — abort instead (empty map or broken enemy functions)
execute if score #mi_total_enemies {ns}.data matches ..0 run tellraw @a [{MGS_TAG},{{"text":"No enemies could be spawned — check the map's enemy markers/functions in the editor.","color":"red"}}]
execute if score #mi_total_enemies {ns}.data matches ..0 run return run function {ns}:v{version}/missions/stop

# Run map-defined start commands after enemies are spawned
execute if data storage {ns}:missions game.map.start_commands[0] run function {ns}:v{version}/shared/run_start_commands {{mode:"missions"}}

# Call map start scripts (state is now active, chunks had time to load)
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"start"}}

# Give compass pointing to nearest enemy (hotbar slot 3)
execute as @a[scores={{{ns}.mi.in_game=1}}] run item replace entity @s hotbar.3 with compass[custom_data={{{ns}:{{compass:true}}}}]

# Reset mission timer (counts up)
scoreboard players set #mi_timer {ns}.data 0

# Announce
tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"GO! GO! GO! Kill all enemies!"}}]
""")

	## Spawn all enemies at once from map data
	write_versioned_function("missions/spawn_all_enemies", f"""
# Copy enemy list for iteration
data modify storage {ns}:temp _enemy_iter set from storage {ns}:missions game.map.enemies

# Start iteration
execute if data storage {ns}:temp _enemy_iter[0] run function {ns}:v{version}/missions/spawn_enemy_iter

# Tag all newly spawned armed mobs as mission enemies
execute as @e[tag={ns}.armed,tag=!{ns}.mission_enemy] run tag @s add {ns}.mission_enemy
execute as @e[tag={ns}.mission_enemy] run tag @s add {ns}.gm_entity
team join {ns}.mi_mobs @e[tag={ns}.mission_enemy]

# Store total enemy count
execute store result score #mi_total_enemies {ns}.data if entity @e[tag={ns}.mission_enemy]

# Announce count
tellraw @a [{MGS_TAG},{{"score":{{"name":"#mi_total_enemies","objective":"{ns}.data"}},"color":"yellow"}}," ",{{"text":"enemies spawned!","color":"gray"}}]
""")

	## Spawn enemy iterator
	write_versioned_function("missions/spawn_enemy_iter", f"""
# Read relative position
execute store result score #ex {ns}.data run data get storage {ns}:temp _enemy_iter[0].pos[0]
execute store result score #ey {ns}.data run data get storage {ns}:temp _enemy_iter[0].pos[1]
execute store result score #ez {ns}.data run data get storage {ns}:temp _enemy_iter[0].pos[2]

# Convert to absolute
scoreboard players operation #ex {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ey {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #ez {ns}.data += #gm_base_z {ns}.data

# Store absolute position for macro
execute store result storage {ns}:temp _epos.x double 1 run scoreboard players get #ex {ns}.data
execute store result storage {ns}:temp _epos.y double 1 run scoreboard players get #ey {ns}.data
execute store result storage {ns}:temp _epos.z double 1 run scoreboard players get #ez {ns}.data

# Copy the function path
data modify storage {ns}:temp _epos.function set from storage {ns}:temp _enemy_iter[0].function

# Call the mob function at the absolute position
function {ns}:v{version}/missions/call_enemy_function with storage {ns}:temp _epos

# Next
data remove storage {ns}:temp _enemy_iter[0]
execute if data storage {ns}:temp _enemy_iter[0] run function {ns}:v{version}/missions/spawn_enemy_iter
""")

	## Call the stored mob function at a given position (macro)
	write_versioned_function("missions/call_enemy_function", """
$execute positioned $(x) $(y) $(z) run function $(function)
""")

