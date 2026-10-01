""" Starting a game: map preload, the prep phase and the handoff to round 1. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.lifecycle import GameLifecycle


# Functions
def write_zombies_start() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/start", f"""
{GameLifecycle.game_start_guards(ns, "zombies", "Zombies game")}

# Players join through Manage Players or + Join.
execute unless entity @a[scores={{{ns}.zb.in_game=1}}] run return run tellraw @s [{MGS_TAG},{{"text":"No players have joined the zombies game. Use Manage Players first.","color":"red"}}]

{GameLifecycle.mode_start_map_bootstrap_lines(ns, "zombies", normalize_legacy=False)}

# in_game is the opt-in flag, so it stays. The XP spend tracker is reset too, or the reset reads as points spent (see xp).
scoreboard players set @a {ns}.zb.points 500
scoreboard players set @a {ns}.zb.xp_pts_prev 500
scoreboard players set @a {ns}.zb.xp_spent_acc 0
scoreboard players set @a {ns}.zb.kills 0
scoreboard players set @a {ns}.zb.downs 0
scoreboard players set @a {ns}.zb.passive 0
scoreboard players set @a {ns}.zb.ability 0
scoreboard players set @a {ns}.zb.ability_cd 0
scoreboard players set @a {ns}.zb.horde_cd 0

scoreboard players set #zb_points_kill {ns}.config 50
scoreboard players set #zb_points_hit {ns}.config 10
scoreboard players set #zb_points_knife_kill {ns}.config 130
scoreboard players set #zb_mystery_box_price {ns}.config 950

team join {ns}.zombies @a[scores={{{ns}.zb.in_game=1}}]

# Kills from before the game do not count.
execute as @a run scoreboard players operation @s {ns}.zb.prev_kills = @s {ns}.total_kills

# Prevents false triggers.
scoreboard players set @a {ns}.mp.death_count 0
scoreboard players set @a {ns}.mp.spectate_timer 0

# A stale flag would pause the first round.
scoreboard players set #zb_freeze {ns}.data 0
tag @e[tag={ns}.zb_frozen_ai] remove {ns}.zb_frozen_ai

scoreboard players set @a {ns}.mp.in_game 0
scoreboard players set @a {ns}.mi.in_game 0

{GameLifecycle.regen_enable_lines(ns)}

gamemode spectator @a[scores={{{ns}.zb.in_game=1}}]
gamerule immediate_respawn true
gamerule keep_inventory true
gamerule max_entity_cramming 96
gamerule advance_time false
time set 18000

# The first round is 1.
data modify storage {ns}:zombies game.round set value 0

function {ns}:v{version}/shared/load_base_coordinates {{mode:"zombies"}}

# At least 2 corners: a lone corner would collapse to a point that eliminates everyone.
scoreboard players set #zb_has_bounds {ns}.data 0
execute if data storage {ns}:zombies game.map.boundaries[0] if data storage {ns}:zombies game.map.boundaries[1] run scoreboard players set #zb_has_bounds {ns}.data 1

execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/shared/load_bounds {{mode:"zombies"}}

execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/shared/forceload_area

# Spectators at the base coordinates while chunks preload.
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #gm_base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #gm_base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #gm_base_z {ns}.data
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/shared/tp_to_position with storage {ns}:temp _tp

# Extension points.
function #{ns}:zombies/register_maps
function #{ns}:zombies/register_mystery_box_item

{GameLifecycle.schedule_preload_complete_line(ns, "zombies")}

tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Loading zombies map...","color":"yellow"}}]
""")

	write_versioned_function("zombies/preload_complete", f"""
execute unless data storage {ns}:zombies game{{state:"preparing"}} run return fail

gamemode adventure @a[scores={{{ns}.zb.in_game=1}}]

execute if data storage {ns}:zombies game.map.out_of_bounds run function {ns}:v{version}/shared/summon_oob {{mode:"zombies"}}

function {ns}:v{version}/zombies/summon_spawns

function #{ns}:zombies/on_game_start

# After the entity and setup summons.
execute if data storage {ns}:zombies game.map.start_commands[0] run function {ns}:v{version}/shared/run_start_commands {{mode:"zombies"}}

function {ns}:v{version}/zombies/tp_all_to_spawns

{GameLifecycle.prep_freeze_lines(ns, "zb")}
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:max_health base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:entity_interaction_range base set 5

execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/inventory/give_starting_loadout

# Zonweeb only.
execute if data storage {ns}:zombies game{{variant:"zonweeb"}} as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/passive_ability_menu

# Prep lasts 10 s.
schedule function {ns}:v{version}/zombies/end_prep 200t

function {ns}:v{version}/zombies/create_sidebar

# Perk wording only for Zonweeb.
execute if data storage {ns}:zombies game{{variant:"zonweeb"}} run tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Preparing! Choose your perk! Round 1 starts in 10 seconds!","color":"yellow"}}]
execute unless data storage {ns}:zombies game{{variant:"zonweeb"}} run tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Preparing! Round 1 starts in 10 seconds!","color":"yellow"}}]
""")

	write_versioned_function("zombies/end_prep", f"""
{GameLifecycle.end_prep_transition_lines(ns, "zombies", "zb")}

function {ns}:v{version}/zombies/start_round

# The state is now active and chunks had time to load.
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"start"}}
""")

