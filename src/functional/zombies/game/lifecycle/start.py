""" Starting a game: map preload, the prep phase and the handoff to round 1. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.lifecycle import GameLifecycle


# Functions
def write_zombies_start() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Game Start
	write_versioned_function("zombies/start", f"""
# Prevent starting if already active or preparing
{GameLifecycle.game_start_guards(ns, "zombies", "Zombies game")}

# Require at least one opted-in player (players are independent until added via Manage Players / + Join)
execute unless entity @a[scores={{{ns}.zb.in_game=1}}] run return run tellraw @s [{MGS_TAG},{{"text":"No players have joined the zombies game — use Manage Players first.","color":"red"}}]

{GameLifecycle.mode_start_map_bootstrap_lines(ns, "zombies", False)}

# Create zombies team
team add {ns}.zombies
team modify {ns}.zombies color yellow
team modify {ns}.zombies friendlyFire false
team modify {ns}.zombies nametagVisibility hideForOtherTeams

# Reset scores (in_game is left untouched: it's the opt-in flag, set via Manage Players / + Join)
# Keep the XP spend tracker in step: an unsynced reset reads as points being SPENT (see zombies/xp.py)
scoreboard players set @a {ns}.zb.points 500
scoreboard players set @a {ns}.zb.xp_pts_prev 500
scoreboard players set @a {ns}.zb.xp_spent_acc 0
scoreboard players set @a {ns}.zb.kills 0
scoreboard players set @a {ns}.zb.downs 0
scoreboard players set @a {ns}.zb.passive 0
scoreboard players set @a {ns}.zb.ability 0
scoreboard players set @a {ns}.zb.ability_cd 0
scoreboard players set @a {ns}.zb.horde_cd 0

# Config: points per kill, points per hit
scoreboard players set #zb_points_kill {ns}.config 50
scoreboard players set #zb_points_hit {ns}.config 5
scoreboard players set #zb_points_knife_kill {ns}.config 130
scoreboard players set #zb_mystery_box_price {ns}.config 950

# Assign opted-in players to the zombies team
team join {ns}.zombies @a[scores={{{ns}.zb.in_game=1}}]

# Initialize kill tracking baseline (so kills before game start don't count)
execute as @a run scoreboard players operation @s {ns}.zb.prev_kills = @s {ns}.total_kills

# Reset death counters and spectate timers to prevent false triggers
scoreboard players set @a {ns}.mp.death_count 0
scoreboard players set @a {ns}.mp.spectate_timer 0

# A game never starts frozen (a stale flag would silently pause the very first round)
scoreboard players set #zb_freeze {ns}.data 0
tag @e[tag={ns}.zb_frozen_ai] remove {ns}.zb_frozen_ai

# Clear other modes' in-game flags so their ticks/logic don't conflict with zombies
scoreboard players set @a {ns}.mp.in_game 0
scoreboard players set @a {ns}.mi.in_game 0

# Disable natural regeneration, enable custom regen system
{GameLifecycle.regen_enable_lines(ns)}

# Set gamerules
gamemode spectator @a[scores={{{ns}.zb.in_game=1}}]
gamerule immediate_respawn true
gamerule keep_inventory true
gamerule max_entity_cramming 96
gamerule advance_time false
time set 18000

# Initialize round to 0 (first round will be 1)
data modify storage {ns}:zombies game.round set value 0

# Store base coordinates for offset
function {ns}:v{version}/shared/load_base_coordinates {{mode:"zombies"}}

# Check if map has boundaries defined (need at least 2 corners to form a box — a lone corner would
# collapse to a degenerate point that eliminates everyone; matches multiplayer/missions)
scoreboard players set #zb_has_bounds {ns}.data 0
execute if data storage {ns}:zombies game.map.boundaries[0] if data storage {ns}:zombies game.map.boundaries[1] run scoreboard players set #zb_has_bounds {ns}.data 1

# Normalize and store boundaries (only if defined)
execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/shared/load_bounds {{mode:"zombies"}}

# Forceload the area (only if bounds defined)
execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/shared/forceload_area

# Teleport all players as spectator to base coordinates for chunk preloading
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #gm_base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #gm_base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #gm_base_z {ns}.data
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/shared/tp_to_position with storage {ns}:temp _tp

# Register custom maps and mystery box items (extension points)
function #{ns}:zombies/register_maps
function #{ns}:zombies/register_mystery_box_item

# Schedule preload completion after 1 second
{GameLifecycle.schedule_preload_complete_line(ns, "zombies")}

# Announce
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Loading zombies map...","color":"yellow"}}]
""")

	## Preload complete → transition to prep phase
	write_versioned_function("zombies/preload_complete", f"""
# Guard: only if still preparing
execute unless data storage {ns}:zombies game{{state:"preparing"}} run return fail

# Switch to adventure mode
gamemode adventure @a[scores={{{ns}.zb.in_game=1}}]

# Summon OOB markers (only if map has out_of_bounds data)
execute if data storage {ns}:zombies game.map.out_of_bounds run function {ns}:v{version}/shared/summon_oob {{mode:"zombies"}}

# Summon spawn point markers for players
function {ns}:v{version}/zombies/summon_spawns

# Signal zombies game start
function #{ns}:zombies/on_game_start

# Run map-defined start commands after entity/setup summons
execute if data storage {ns}:zombies game.map.start_commands[0] run function {ns}:v{version}/shared/run_start_commands {{mode:"zombies"}}

# Teleport all players to player spawns
function {ns}:v{version}/zombies/tp_all_to_spawns

# Freeze players during prep
{GameLifecycle.prep_freeze_lines(ns, "zb")}
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:max_health base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:entity_interaction_range base set 5

# Give starting loadout to all players
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/inventory/give_starting_loadout

# Show zombies passive/ability selection menu (Zonweeb variant only)
execute if data storage {ns}:zombies game{{variant:"zonweeb"}} as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/passive_ability_menu

# Schedule end of prep (10 seconds remaining)
schedule function {ns}:v{version}/zombies/end_prep 200t

# Initialize sidebar
function {ns}:v{version}/zombies/create_sidebar

# Announce (perk wording only applies to Zonweeb)
execute if data storage {ns}:zombies game{{variant:"zonweeb"}} run tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Preparing! Choose your perk! Round 1 starts in 10 seconds!","color":"yellow"}}]
execute unless data storage {ns}:zombies game{{variant:"zonweeb"}} run tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Preparing! Round 1 starts in 10 seconds!","color":"yellow"}}]
""")

	## Prep Tick (no class to detect, just wait)
	write_versioned_function("zombies/prep_tick", """
# Nothing to process during prep (perk selection is instant via chat click)
""")

	## End Prep → Start Round 1
	write_versioned_function("zombies/end_prep", f"""
{GameLifecycle.end_prep_transition_lines(ns, "zombies", "zb")}

# Start round 1
function {ns}:v{version}/zombies/start_round

# Call map start scripts (state is now active, chunks had time to load)
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"start"}}
""")

