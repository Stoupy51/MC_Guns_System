
# ruff: noqa: E501
# Zombies Game System
# Wave-based survival mode with zombie spawning, points, perks, mystery box, wallbuys, doors, and traps.
# Map definitions are dynamic (stored in storage, registered via function tags).
from stewbeet import Mem, write_tag

from ..helpers import (
	MGS_TAG,
	end_prep_transition_lines,
	game_start_guards,
	late_join_flow_lines,
	mode_start_map_bootstrap_lines,
	prep_freeze_lines,
	regen_disable_lines,
	regen_enable_lines,
	schedule_preload_complete_line,
)
from ..game_mode import GameMode


class ZombiesMode(GameMode):
    """ Generates the zombies game lifecycle (rounds, co-op spawns, sidebar). """

    mode = "zombies"

    def generate(self) -> None:
    	ns: str = self.ns
    	version: str = self.version

    	## Scoreboards & Storage Setup
    	self.load(
    f"""
## Zombies scoreboards
scoreboard objectives add {ns}.zb.in_game dummy
scoreboard objectives add {ns}.zb.points dummy
scoreboard objectives add {ns}.zb.kills dummy
scoreboard objectives add {ns}.zb.downs dummy

# Perk scoreboards
# zb.passive: 0=none, 1=points_x1.2, 2=powerup_x1.5
# zb.ability: 0=none, 1=coward, 2=guardian
# Ability cooldown (0 = ready, 1+ = on cooldown in rounds remaining)
scoreboard objectives add {ns}.zb.passive dummy
scoreboard objectives add {ns}.zb.ability dummy
scoreboard objectives add {ns}.zb.ability_cd dummy

# Spawn point group_id scoreboard
scoreboard objectives add {ns}.zb.spawn.gid dummy

# Sidebar rank scoreboard
scoreboard objectives add {ns}.zb.sb_rank dummy

# Rise animation: ticks remaining for each rising zombie
scoreboard objectives add {ns}.zb.rise_tick dummy

# Kill tracking (vanilla totalKillCount stat) and baseline snapshot
scoreboard objectives add {ns}.total_kills totalKillCount
scoreboard objectives add {ns}.zb.prev_kills dummy

# Stuck zombie detection per-zombie scores
scoreboard objectives add {ns}.zb.stuck_x dummy
scoreboard objectives add {ns}.zb.stuck_z dummy
scoreboard objectives add {ns}.zb.stuck_ticks dummy
scoreboard objectives add {ns}.zb.stuck_dist dummy

# Initialize zombies game state
execute unless data storage {ns}:zombies game run data modify storage {ns}:zombies game set value {{state:"lobby",map_id:"",round:0}}

# Game variant: "vanilla" = classic CoD zombies, "zonweeb" = passives/abilities/special zombies
execute unless data storage {ns}:zombies game.variant run data modify storage {ns}:zombies game.variant set value "zonweeb"

# Initialize mystery box base pool (can be extended via function tag)
execute unless data storage {ns}:zombies mystery_box_pool run data modify storage {ns}:zombies mystery_box_pool set value []
""")

    	## Signal function tags
    	for event in ["register_maps", "register_mystery_box_item", "on_round_start", "on_round_end", "on_game_start", "on_game_end"]:
    		write_tag(f"zombies/{event}", Mem.ctx.data[ns].function_tags, [])

    	## Game Start
    	self.func("zombies/start", f"""
# Prevent starting if already active or preparing
{game_start_guards(ns, "zombies", "Zombies game")}

{mode_start_map_bootstrap_lines(ns, "zombies", False)}

# Create zombies team
team add {ns}.zombies
team modify {ns}.zombies color yellow
team modify {ns}.zombies friendlyFire false
team modify {ns}.zombies nametagVisibility hideForOtherTeams

# Reset scores
scoreboard players set @a {ns}.zb.in_game 0
scoreboard players set @a {ns}.zb.points 500
scoreboard players set @a {ns}.zb.kills 0
scoreboard players set @a {ns}.zb.downs 0
scoreboard players set @a {ns}.zb.passive 0
scoreboard players set @a {ns}.zb.ability 0
scoreboard players set @a {ns}.zb.ability_cd 0

# Config: points per kill, points per hit
scoreboard players set #zb_points_kill {ns}.config 50
scoreboard players set #zb_points_hit {ns}.config 5
scoreboard players set #zb_points_knife_kill {ns}.config 130
scoreboard players set #zb_mystery_box_price {ns}.config 950

# Tag all players as in-game
scoreboard players set @a {ns}.zb.in_game 1

# Assign all in-game players to zombies team
team join {ns}.zombies @a[scores={{{ns}.zb.in_game=1}}]

# Initialize kill tracking baseline (so kills before game start don't count)
execute as @a run scoreboard players operation @s {ns}.zb.prev_kills = @s {ns}.total_kills

# Reset death counters and spectate timers to prevent false triggers
scoreboard players set @a {ns}.mp.death_count 0
scoreboard players set @a {ns}.mp.spectate_timer 0

# Clear other modes' in-game flags so their ticks/logic don't conflict with zombies
scoreboard players set @a {ns}.mp.in_game 0
scoreboard players set @a {ns}.mi.in_game 0

# Disable natural regeneration, enable custom regen system
{regen_enable_lines(ns)}

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

# Check if map has boundaries defined
scoreboard players set #zb_has_bounds {ns}.data 0
execute if data storage {ns}:zombies game.map.boundaries[0] run scoreboard players set #zb_has_bounds {ns}.data 1

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
{schedule_preload_complete_line(ns, "zombies")}

# Announce
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Loading zombies map...","color":"yellow"}}]
""")

    	## Preload complete → transition to prep phase
    	self.func("zombies/preload_complete", f"""
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
{prep_freeze_lines(ns, "zb")}
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
    	self.func("zombies/prep_tick", """
# Nothing to process during prep (perk selection is instant via chat click)
""")

    	## End Prep → Start Round 1
    	self.func("zombies/end_prep", f"""
{end_prep_transition_lines(ns, "zombies", "zb")}

# Start round 1
function {ns}:v{version}/zombies/start_round

# Call map start scripts (state is now active, chunks had time to load)
function {ns}:v{version}/shared/maps/call_start_script_at_base
""")


    	# Game Tick ─────────────────────────────────────────────────

    	self.tick(f"""
# Zombies game tick
execute if data storage {ns}:zombies game{{state:"active"}} run function {ns}:v{version}/zombies/game_tick
execute if data storage {ns}:zombies game{{state:"preparing"}} run function {ns}:v{version}/zombies/prep_tick
""")

    	self.func("zombies/game_tick", f"""
# Revive system tick (process downed players)
function {ns}:v{version}/zombies/revive/tick

# Call map-defined tick script
function {ns}:v{version}/shared/maps/call_tick_script_at_base

# Zombie Spawning (if there are still zombies to spawn)
execute if score #zb_to_spawn {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_tick

# Rise animation tick for spawning zombies
execute as @e[tag={ns}.zb_rising] at @s run function {ns}:v{version}/zombies/zombie_rise_tick

# Boundary enforcement (skip spectators, only if map has bounds)
execute if score #zb_has_bounds {ns}.data matches 1 as @e[tag={ns}.zombie_round] at @s run function {ns}:v{version}/shared/check_bounds
execute if score #zb_has_bounds {ns}.data matches 1 as @e[type=player,scores={{{ns}.zb.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/shared/check_bounds

# Check round completion
execute store result score #zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]
execute if score #zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 run function {ns}:v{version}/zombies/round_complete

# Check game over: only trigger when no healthy AND no downed players remain
# - Healthy: downed=0, gamemode=!spectator (playing normally)
# - Downed: downed=1, gamemode=spectator (spectating their mannequin, can be revived)
# - Bled out: downed=0, gamemode=spectator (waiting for next round — truly dead)
execute if score #zb_round_grace {ns}.data matches 1.. run scoreboard players remove #zb_round_grace {ns}.data 1
execute unless score #zb_round_grace {ns}.data matches 1.. store result score #zb_alive_players {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]
execute unless score #zb_round_grace {ns}.data matches 1.. store result score #zb_downed_alive {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=1}},gamemode=spectator]
execute unless score #zb_round_grace {ns}.data matches 1.. run scoreboard players operation #zb_alive_players {ns}.data += #zb_downed_alive {ns}.data
execute unless score #zb_round_grace {ns}.data matches 1.. if score #zb_alive_players {ns}.data matches 0 run function {ns}:v{version}/zombies/game_over

# Stuck zombie check (every 20 ticks, 24 random non-rising zombies)
execute store result score #zb_tick_mod {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #zb_tick_mod {ns}.data %= #20 {ns}.data
execute if score #zb_tick_mod {ns}.data matches 0 as @e[tag={ns}.zombie_round,tag=!{ns}.zb_rising,limit=24,sort=random] at @s run function {ns}:v{version}/zombies/stuck_zombie_check

# Stuck zombie glow: count up once all spawns are done (60s = 1200 ticks after last spawn)
execute if score #zb_to_spawn {ns}.data matches 0 run scoreboard players add #zb_stuck_timer {ns}.data 1
execute if score #zb_to_spawn {ns}.data matches 1.. run scoreboard players set #zb_stuck_timer {ns}.data 0
# Once threshold reached, tick glow refresh timer (every 5s = 100 ticks → apply glowing for 6s = 120 ticks)
execute if score #zb_stuck_timer {ns}.data matches 1200.. run scoreboard players add #zb_glow_timer {ns}.data 1
execute if score #zb_glow_timer {ns}.data matches 100.. run scoreboard players set #zb_glow_timer {ns}.data 0
execute if score #zb_stuck_timer {ns}.data matches 1200.. if score #zb_glow_timer {ns}.data matches 0 if entity @e[tag={ns}.zombie_round] run function {ns}:v{version}/zombies/glow_stuck_zombies

# Refresh sidebar every second (20 ticks)
scoreboard players add #zb_sidebar_timer {ns}.data 1
execute if score #zb_sidebar_timer {ns}.data matches 20.. run scoreboard players set #zb_sidebar_timer {ns}.data 0
execute if score #zb_sidebar_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/refresh_sidebar

# Cleanup
kill @e[type=experience_orb]
""")


    	# Death & Respawn ───────────────────────────────────────────
    	## On Respawn (zombies death handling → enter downed state)
    	self.func("zombies/on_respawn", f"""
# Reset death counter
scoreboard players set @s {ns}.mp.death_count 0

# Increment down count
scoreboard players add @s {ns}.zb.downs 1

# Enter downed state (revive system)
function {ns}:v{version}/zombies/revive/on_down
""")

    	## Add player tick hook for zombies death detection
    	self.func("player/tick", f"""
# Zombies: detect respawn
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/zombies/on_respawn
""")

    	# Game Over ─────────────────────────────────────────────────

    	self.func("zombies/game_over", f"""
# Set state to ended
data modify storage {ns}:zombies game.state set value "ended"

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 80 20
title @a[scores={{{ns}.zb.in_game=1}}] title {{"text":"GAME OVER","color":"dark_red","bold":true}}

# Calculate final round
execute store result score #final_round {ns}.data run data get storage {ns}:zombies game.round

# Performance summary
tellraw @a ["","\\n",{{"text":"═══════ GAME OVER ═══════","color":"dark_red","bold":true}}]
tellraw @a ["","  ",{{"text":"🧟 Final Round: ","color":"gray"}},{{"score":{{"name":"#final_round","objective":"{ns}.data"}},"color":"red","bold":true}}]

# Per-player stats
execute as @a[scores={{{ns}.zb.in_game=1}}] run tellraw @a ["","  ",{{"text":"🎖 ","color":"gray"}},{{"selector":"@s","color":"yellow"}}," — Kills: ",{{"score":{{"name":"@s","objective":"{ns}.zb.kills"}},"color":"green"}}," | Downs: ",{{"score":{{"name":"@s","objective":"{ns}.zb.downs"}},"color":"red"}}," | Points: ",{{"score":{{"name":"@s","objective":"{ns}.zb.points"}},"color":"gold"}}]

tellraw @a ["",{{"text":"═════════════════════════","color":"dark_red","bold":true}},"\\n"]

# Signal game end
function #{ns}:zombies/on_game_end

# Stop all sounds and play gameover sound
stopsound @a
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/game_over ambient @s ~ ~ ~ 0.6 1.0

# End game after 5 seconds
schedule function {ns}:v{version}/zombies/stop 100t
""")

    	# Game Stop ─────────────────────────────────────────────────
    	self.func("zombies/stop", f"""
# Various cleanup to set to lobby state
data modify storage {ns}:zombies game.state set value "lobby"
schedule clear {ns}:v{version}/zombies/end_prep
schedule clear {ns}:v{version}/zombies/start_round
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:max_health base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:entity_interaction_range base reset
effect clear @a[scores={{{ns}.zb.in_game=1}}] darkness
effect clear @a[scores={{{ns}.zb.in_game=1}}] blindness
effect clear @a[scores={{{ns}.zb.in_game=1}}] night_vision
gamemode adventure @a[scores={{{ns}.zb.in_game=1}},gamemode=spectator]
kill @e[tag={ns}.zombie_round]
kill @e[tag={ns}.gm_entity]

# Remove forceload (only if bounds were set)
execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/shared/remove_forceload

scoreboard objectives setdisplay sidebar
scoreboard objectives remove {ns}.zb_sidebar
gamerule advance_time true

{regen_disable_lines(ns)}

# Announce
tellraw @a [{MGS_TAG},{{"text":"Zombies game ended.","color":"red"}}]
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/shared/maps/call_leave_script_at_base

# Reset in-game state
scoreboard players set @a {ns}.zb.in_game 0
scoreboard players set @a {ns}.zb.points 0
scoreboard players set @a {ns}.zb.kills 0
scoreboard players set @a {ns}.zb.downs 0
scoreboard players set @a {ns}.zb.passive 0
scoreboard players set @a {ns}.zb.ability 0
scoreboard players set @a {ns}.zb.ability_cd 0
scoreboard players set @a {ns}.zb.prev_kills 0
scoreboard players set @a {ns}.mp.spectate_timer 0
tag @a[tag={ns}.give_class_menu] remove {ns}.give_class_menu
""")

    	## Join Ongoing Zombies Game (late-joiner support)
    	self.func("zombies/join_game", f"""
{late_join_flow_lines(
	ns,
	"zombies",
	f"{ns}.zb.in_game",
	"No active zombies game to join!",
	"You are already in the zombies game!",
	f"""
scoreboard players set @s {ns}.zb.in_game 1
team join {ns}.zombies @s
scoreboard players set @s {ns}.zb.points 500
scoreboard players set @s {ns}.zb.kills 0
scoreboard players set @s {ns}.zb.downs 0
scoreboard players set @s {ns}.zb.passive 0
scoreboard players set @s {ns}.zb.ability 0
scoreboard players set @s {ns}.zb.ability_cd 0
scoreboard players set @s {ns}.mp.spectate_timer 0
scoreboard players set @s {ns}.mp.death_count 0
attribute @s minecraft:max_health base reset
attribute @s minecraft:entity_interaction_range base set 5
""",
	f"{ns}:v{version}/zombies/respawn_tp",
	"joined the zombies game!",
	"dark_green",
	post_class_lines=f"scoreboard players operation @s {ns}.zb.prev_kills = @s {ns}.total_kills",
)}
""")

    	# Kill Points ───────────────────────────────────────────────
    	# Track kills via totalKillCount stat delta — catches all kill types (bullets, knife, etc.)
    	self.func("zombies/check_kill_points", f"""
# Calculate delta kills since last check
scoreboard players operation #zb_kills_delta {ns}.data = @s {ns}.total_kills
scoreboard players operation #zb_kills_delta {ns}.data -= @s {ns}.zb.prev_kills
scoreboard players operation @s {ns}.zb.prev_kills = @s {ns}.total_kills

# Skip if no new kills
execute if score #zb_kills_delta {ns}.data matches ..0 run return 0

# Determine kill type: gun (bullet kill = 50) or melee (knife kill = 130)
scoreboard players set #zb_kill_points {ns}.data 0
execute if items entity @s weapon.mainhand *[custom_data~{{{ns}:{{gun:true}}}}] run scoreboard players operation #zb_kill_points {ns}.data = #zb_points_kill {ns}.config
execute unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{gun:true}}}}] run scoreboard players operation #zb_kill_points {ns}.data = #zb_points_knife_kill {ns}.config

# Award base points (delta * points_per_kill_type)
scoreboard players operation #total_kill_points {ns}.data = #zb_kills_delta {ns}.data
scoreboard players operation #total_kill_points {ns}.data *= #zb_kill_points {ns}.data
scoreboard players operation @s {ns}.zb.points += #total_kill_points {ns}.data

# Apply x1.2 points passive: add 20% extra
execute if score @s {ns}.zb.passive matches 1 run scoreboard players operation #additional {ns}.data = #total_kill_points {ns}.data
execute if score @s {ns}.zb.passive matches 1 run scoreboard players operation #additional {ns}.data /= #5 {ns}.data
execute if score @s {ns}.zb.passive matches 1 run scoreboard players operation @s {ns}.zb.points += #additional {ns}.data

# Accumulate kill count
scoreboard players operation @s {ns}.zb.kills += #zb_kills_delta {ns}.data

# Refresh sidebar
function {ns}:v{version}/zombies/refresh_sidebar
""")

    	# Bullet hit points (+10 per bullet hit on a live zombie)
    	self.func("zombies/on_hit_signal", f"""
# Only process if zombies game is active & If the hit target is a live round zombie
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute unless entity @s[tag={ns}.zombie_round] run return fail

# Mark this zombie as hit by a player this tick (gates power-up drops to player kills)
scoreboard players operation @s {ns}.zb.player_hit = #total_tick {ns}.data

# Award +10 bullet hit points to the shooter
scoreboard players operation @n[tag={ns}.ticking] {ns}.zb.points += #zb_points_hit {ns}.config

# Refresh sidebar
function {ns}:v{version}/zombies/refresh_sidebar
""", tags=[f"{ns}:signals/damage"])

    	# Hook kill check into game_tick (per in-game player, non-spectator)
    	self.func("zombies/game_tick", f"""
# Award kill points from totalKillCount delta
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:v{version}/zombies/check_kill_points
""")


    	# Stuck Zombie Check ────────────────────────────────────────
    	self.func("zombies/stuck_zombie_check", f"""
# @s = zombie_round entity (non-rising), run every 20 ticks on up to 24 random zombies
# Progress = distance bucket improved OR XZ position changed. Either resets the timer.

# Compute distance bucket to nearest alive player (4=very far, 0=adjacent)
scoreboard players set #cur_dist_bucket {ns}.data 4
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..96] run scoreboard players set #cur_dist_bucket {ns}.data 3
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..64] run scoreboard players set #cur_dist_bucket {ns}.data 2
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..32] run scoreboard players set #cur_dist_bucket {ns}.data 1
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..16] run scoreboard players set #cur_dist_bucket {ns}.data 0

# Compute current XZ position
execute store result score #cur_x {ns}.data run data get entity @s Pos[0]
execute store result score #cur_z {ns}.data run data get entity @s Pos[2]

# Detect any progress: bucket improved, OR bucket == 0 (zombie is in melee range — not stuck)
# XZ movement is NOT checked: a zombie attacking at close range stands still legitimately
scoreboard players set #stuck_progress {ns}.data 0
execute if score #cur_dist_bucket {ns}.data < @s {ns}.zb.stuck_dist run scoreboard players set #stuck_progress {ns}.data 1
execute if score #cur_dist_bucket {ns}.data matches 0 run scoreboard players set #stuck_progress {ns}.data 1

# If progress: update all stored values and reset timestamp
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_dist = #cur_dist_bucket {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_x = #cur_x {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_z = #cur_z {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data

# If no progress: compute elapsed ticks; respawn if >= 300 (15s)
execute if score #stuck_progress {ns}.data matches 0 run scoreboard players operation #stuck_delta {ns}.data = #total_tick {ns}.data
execute if score #stuck_progress {ns}.data matches 0 run scoreboard players operation #stuck_delta {ns}.data -= @s {ns}.zb.stuck_ticks
execute if score #stuck_progress {ns}.data matches 0 if score #stuck_delta {ns}.data matches 300.. run function {ns}:v{version}/zombies/on_stuck_zombie
""")

    	self.func("zombies/on_stuck_zombie", f"""
# @s = stuck zombie — teleport it to a zombie spawn point near a player instead of killing it
# (keeps the horde intact and drops it back onto walkable navmesh so it can path again).

# Build the rescue pool: unlocked zombie spawn markers near any in-game player — same selection
# the spawner uses (within 32, widening to 64, then any unlocked spawn as a final fallback).
tag @e[tag={ns}.spawn_zb] remove {ns}.zb_rescue
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked,distance=..32] add {ns}.zb_rescue
execute unless entity @e[tag={ns}.zb_rescue] as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked,distance=..64] add {ns}.zb_rescue
execute unless entity @e[tag={ns}.zb_rescue] run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked] add {ns}.zb_rescue

# Teleport to the nearest rescue spawn (passenger death_watch marker follows automatically)
execute if entity @e[tag={ns}.zb_rescue] run tp @s @n[tag={ns}.zb_rescue]
tag @e[tag={ns}.zb_rescue] remove {ns}.zb_rescue

# Reset stuck tracking from the new position so it gets a fresh window
scoreboard players set @s {ns}.zb.stuck_dist 4
execute store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
""")

    	# Spawn Point Markers ───────────────────────────────────────

    	self.func("zombies/summon_spawns", f"""
# Player spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.players
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_zb_player"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter

# Zombie spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.zombies
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_zb"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter

# Tag group 0 spawns as unlocked (starting area)
scoreboard players set #unlock_gid {ns}.data 0
execute as @e[tag={ns}.spawn_point] if score @s {ns}.zb.spawn.gid = #unlock_gid {ns}.data run tag @s add {ns}.spawn_unlocked
""")

    	self.func("zombies/summon_spawn_iter", f"""
# Read position from compound format
execute store result score #sx {ns}.data run data get storage {ns}:temp _spawn_iter[0].pos[0]
execute store result score #sy {ns}.data run data get storage {ns}:temp _spawn_iter[0].pos[1]
execute store result score #sz {ns}.data run data get storage {ns}:temp _spawn_iter[0].pos[2]
execute store result score #syaw {ns}.data run data get storage {ns}:temp _spawn_iter[0].rotation[0] 100

scoreboard players operation #sx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #sy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #sz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #sx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #sy {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #sz {ns}.data
execute store result storage {ns}:temp _spos.yaw double 0.01 run scoreboard players get #syaw {ns}.data
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_tag

function {ns}:v{version}/zombies/summon_spawn_at with storage {ns}:temp _spos

# Set group_id score on newly spawned marker (default 0 if not defined)
scoreboard players set @n[tag={ns}.new_spawn] {ns}.zb.spawn.gid 0
execute store result score @n[tag={ns}.new_spawn] {ns}.zb.spawn.gid run data get storage {ns}:temp _spawn_iter[0].group_id
tag @n[tag={ns}.new_spawn] remove {ns}.new_spawn

data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter
""")

    	self.write_summon_spawn_at(extra_spawn_tags=("new_spawn",))

    	# Smart Spawn Selection ─────────────────────────────────────

    	self.func("zombies/tp_all_to_spawns", f"""
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/pick_spawn
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

    	self.func("zombies/pick_spawn", f"""
tag @s add {ns}.spawn_pending

# Tag candidate spawns (unlocked, exclude used)
tag @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked,tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# If all used, re-tag all unlocked
execute unless entity @e[tag={ns}.spawn_candidate] run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate

# Pick random candidate
execute as @n[tag={ns}.spawn_candidate,sort=random] run function {ns}:v{version}/zombies/tp_to_spawn

# Cleanup
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
""")

    	self.func("zombies/tp_to_spawn", f"""
execute store result storage {ns}:temp _tp.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _tp.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _tp.z double 1 run data get entity @s Pos[2]
data modify storage {ns}:temp _tp.yaw set from entity @s data.yaw

execute as @p[tag={ns}.spawn_pending] run function {ns}:v{version}/zombies/tp_player_at with storage {ns}:temp _tp

execute unless data storage {ns}:zombies game{{state:"active"}} run tag @s add {ns}.spawn_used
""")

    	self.write_tp_player_at()

    	## Respawn TP for zombies
    	self.func("zombies/respawn_tp", f"""
execute if entity @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player] run function {ns}:v{version}/zombies/pick_spawn
""")

    	# Sidebar HUD ───────────────────────────────────────────────
    	self.func("zombies/create_sidebar", f"""
scoreboard objectives add {ns}.zb_sidebar dummy
function {ns}:v{version}/zombies/refresh_sidebar
scoreboard objectives setdisplay sidebar {ns}.zb_sidebar
""")

    	self.func("zombies/refresh_sidebar", f"""
# Count alive zombies
execute store result score #zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]
scoreboard players operation #zb_total {ns}.data = #zb_alive {ns}.data
scoreboard players operation #zb_total {ns}.data += #zb_to_spawn {ns}.data
execute if score #zb_total {ns}.data matches ..-1 run scoreboard players set #zb_total {ns}.data 0

# Initialize sidebar contents
data modify storage {ns}:temp zb_sb set value [[{{text:"Round",color:"red"}},{{score:{{name:"#zb_round",objective:"{ns}.data"}},color:"gold"}}],[{{text:"Zombies",color:"red"}},{{score:{{name:"#zb_total",objective:"{ns}.data"}},color:"gold"}}]," "]

# Rank players for sidebar display
scoreboard players set @a {ns}.zb.sb_rank 0
tag @a remove {ns}.zb_sb_cand
tag @a[scores={{{ns}.zb.in_game=1}}] add {ns}.zb_sb_cand
function {ns}:v{version}/zombies/sidebar_rank_players

# Build sidebar via macro
function {ns}:v{version}/zombies/build_sidebar with storage {ns}:temp
""")

    	# Rank players and append to sidebar (up to 8 players)
    	sidebar_rank_code = ""
    	for i in range(1, 9):
    		sidebar_rank_code += f"""
execute unless entity @a[tag={ns}.zb_sb_cand] run return 0
execute as @a[tag={ns}.zb_sb_cand,limit=1] run scoreboard players set @s {ns}.zb.sb_rank {i}
tag @a[scores={{{ns}.zb.sb_rank={i}}}] remove {ns}.zb_sb_cand
data modify storage {ns}:temp zb_sb append value [{{selector:"@a[scores={{{ns}.zb.sb_rank={i}}}]",color:"green"}},{{score:{{name:"@a[scores={{{ns}.zb.sb_rank={i}}}]",objective:"{ns}.zb.points"}},color:"yellow"}}]
"""
    	sidebar_rank_code += f"\ntag @a remove {ns}.zb_sb_cand\n"
    	self.func("zombies/sidebar_rank_players", sidebar_rank_code)

    	self.func("zombies/build_sidebar", f"""
scoreboard players reset * {ns}.zb_sidebar
$function #bs.sidebar:create {{objective:"{ns}.zb_sidebar",display_name:{{text:"Zombies",color:"dark_green",bold:true}},contents:$(zb_sb)}}
""")

    	# Block shooting during prep
    	self.func("player/right_click", f"""
# Block shooting during zombies prep phase
execute if score @s {ns}.zb.in_game matches 1 if data storage {ns}:zombies game{{state:"preparing"}} run return run scoreboard players set @s {ns}.pending_clicks 0
""", prepend=True)


def generate_zombies_game() -> None:
	""" Module-level entry (preserved signature); delegates to :class:`ZombiesMode`. """
	ZombiesMode()()


