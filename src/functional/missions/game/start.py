""" Starting a mission: map preload, the prep phase and spawning every enemy. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG
from ...helpers.lifecycle import GameLifecycle


# Functions
def write_missions_start() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("missions/start", f"""
{GameLifecycle.game_start_guards(ns, "missions", "Mission")}

# Players join through Manage Players or + Join.
execute unless entity @a[scores={{{ns}.mi.in_game=1}}] run return run tellraw @s [{MGS_TAG},{{"text":"No players have joined the mission — use Manage Players first.","color":"red"}}]

{GameLifecycle.mode_start_map_bootstrap_lines(ns, "missions", normalize_legacy=True)}

# in_game is the opt-in flag, so it stays.
scoreboard players set #mi_timer {ns}.data 0
scoreboard players set #mi_total_enemies {ns}.data 0
scoreboard players set #mi_has_boundary {ns}.data 0
scoreboard players set @a {ns}.mi.kills 0
scoreboard players set @a {ns}.mi.deaths 0
scoreboard players set @a {ns}.mp.spectate_timer 0

# deathCount keeps counting outside games: a lobby death would fire missions/on_respawn the moment the state turns active.
scoreboard players set @a {ns}.mp.death_count 0

scoreboard players set @a[scores={{{ns}.mi.in_game=1}}] {ns}.mp.team 1
team join {ns}.blue @a[scores={{{ns}.mi.in_game=1}}]

tag @a[scores={{{ns}.mi.in_game=1}}] add {ns}.give_class_menu

# Baseline for the per-mission kill count.
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mi.kill_base = @s {ns}.mi.kill_total

gamemode spectator @a[scores={{{ns}.mi.in_game=1}}]
gamerule immediate_respawn true
gamerule keep_inventory true

{GameLifecycle.regen_enable_lines(ns)}

function {ns}:v{version}/shared/load_base_coordinates {{mode:"missions"}}

# Needs 2 points.
execute if data storage {ns}:missions game.map.boundaries[0] if data storage {ns}:missions game.map.boundaries[1] run scoreboard players set #mi_has_boundary {ns}.data 1

execute if score #mi_has_boundary {ns}.data matches 1 run function {ns}:v{version}/shared/load_bounds {{mode:"missions"}}

execute if score #mi_has_boundary {ns}.data matches 1 run function {ns}:v{version}/shared/forceload_area

# Spectators at the base coordinates while chunks preload.
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #gm_base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #gm_base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #gm_base_z {ns}.data
execute as @a[scores={{{ns}.mi.in_game=1}}] run function {ns}:v{version}/shared/tp_to_position with storage {ns}:temp _tp

{GameLifecycle.schedule_preload_complete_line(ns, "missions")}

tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"Loading mission area...","color":"yellow"}}]
""")

	write_versioned_function("missions/preload_complete", f"""
execute unless data storage {ns}:missions game{{state:"preparing"}} run return fail

gamemode adventure @a[scores={{{ns}.mi.in_game=1}}]

function {ns}:v{version}/shared/summon_oob {{mode:"missions"}}

function {ns}:v{version}/missions/summon_spawns

function #{ns}:missions/on_mission_start

function {ns}:v{version}/missions/tp_all_to_spawns

{GameLifecycle.prep_freeze_lines(ns, "mi")}
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:waypoint_receive_range base reset

execute as @a[scores={{{ns}.mi.in_game=1}}] at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# `add 0` initializes unset scores, so the `matches 0` test below can succeed.
scoreboard players add @a {ns}.mp.class 0
execute as @a[scores={{{ns}.mi.in_game=1}}] at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default

execute as @a[scores={{{ns}.mi.in_game=1}}] run function {ns}:v{version}/multiplayer/select_class

# For change detection during prep.
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class

# Prep lasts 9 s.
schedule function {ns}:v{version}/missions/end_prep 180t

tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"Preparing! Choose your class! Mission starts in 9 seconds!","color":"yellow"}}]
""")

	## Re-applies a class changed during prep.
	write_versioned_function("missions/prep_tick", f"""
execute as @a[scores={{{ns}.mi.in_game=1}}] unless score @s {ns}.mp.prev_class = @s {ns}.mp.class at @s run function {ns}:v{version}/multiplayer/apply_class
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class
""")

	write_versioned_function("missions/end_prep", f"""
{GameLifecycle.end_prep_transition_lines(ns, "missions", "mi")}

function {ns}:v{version}/missions/spawn_all_enemies

# A mission with no enemies would complete at once (empty map or broken enemy functions).
execute if score #mi_total_enemies {ns}.data matches ..0 run tellraw @a [{MGS_TAG},{{"text":"No enemies could be spawned — check the map's enemy markers/functions in the editor.","color":"red"}}]
execute if score #mi_total_enemies {ns}.data matches ..0 run return run function {ns}:v{version}/missions/stop

# After the enemies spawn.
execute if data storage {ns}:missions game.map.start_commands[0] run function {ns}:v{version}/shared/run_start_commands {{mode:"missions"}}

# The state is now active and chunks had time to load.
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"start"}}

# Points to the nearest enemy.
execute as @a[scores={{{ns}.mi.in_game=1}}] run item replace entity @s hotbar.3 with compass[custom_data={{{ns}:{{compass:true}}}}]

# Counts up.
scoreboard players set #mi_timer {ns}.data 0

tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"GO! GO! GO! Kill all enemies!"}}]
""")

	write_versioned_function("missions/spawn_all_enemies", f"""
data modify storage {ns}:temp _enemy_iter set from storage {ns}:missions game.map.enemies

execute if data storage {ns}:temp _enemy_iter[0] run function {ns}:v{version}/missions/spawn_enemy_iter

execute as @e[tag={ns}.armed,tag=!{ns}.mission_enemy] run tag @s add {ns}.mission_enemy
execute as @e[tag={ns}.mission_enemy] run tag @s add {ns}.gm_entity
team join {ns}.mi_mobs @e[tag={ns}.mission_enemy]

execute store result score #mi_total_enemies {ns}.data if entity @e[tag={ns}.mission_enemy]

tellraw @a [{MGS_TAG},{{"score":{{"name":"#mi_total_enemies","objective":"{ns}.data"}},"color":"yellow"}}," ",{{"text":"enemies spawned!","color":"gray"}}]
""")

	write_versioned_function("missions/spawn_enemy_iter", f"""
execute store result score #ex {ns}.data run data get storage {ns}:temp _enemy_iter[0].pos[0]
execute store result score #ey {ns}.data run data get storage {ns}:temp _enemy_iter[0].pos[1]
execute store result score #ez {ns}.data run data get storage {ns}:temp _enemy_iter[0].pos[2]

scoreboard players operation #ex {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ey {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #ez {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _epos.x double 1 run scoreboard players get #ex {ns}.data
execute store result storage {ns}:temp _epos.y double 1 run scoreboard players get #ey {ns}.data
execute store result storage {ns}:temp _epos.z double 1 run scoreboard players get #ez {ns}.data

data modify storage {ns}:temp _epos.function set from storage {ns}:temp _enemy_iter[0].function

function {ns}:v{version}/missions/call_enemy_function with storage {ns}:temp _epos

data remove storage {ns}:temp _enemy_iter[0]
execute if data storage {ns}:temp _enemy_iter[0] run function {ns}:v{version}/missions/spawn_enemy_iter
""")

	write_versioned_function("missions/call_enemy_function", """
$execute positioned $(x) $(y) $(z) run function $(function)
""")

