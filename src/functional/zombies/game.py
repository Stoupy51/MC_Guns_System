
# ruff: noqa: E501
# Zombies Game System
# Wave-based survival mode with zombie spawning, points, perks, mystery box, wallbuys, doors, and traps.
# Map definitions are dynamic (stored in storage, registered via function tags).
from stewbeet import Mem, write_tag, write_versioned_function

from ..game_mode import GameMode
from ..helpers import (
	MGS_TAG,
	btn,
	end_prep_transition_lines,
	game_start_guards,
	late_join_flow_lines,
	mode_start_map_bootstrap_lines,
	prep_freeze_lines,
	regen_disable_lines,
	regen_enable_lines,
	schedule_preload_complete_line,
	write_ranked_stats_functions,
)


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

# Bought lethal grenade type (index into LETHAL_GRENADE_IDS, 0 = frag): re-gives the RIGHT type
# when the lethal slot is emptied (round-end replenish / Max Ammo / recovery). See inventory.py.
scoreboard objectives add {ns}.zb.lethal_type dummy

# Perk scoreboards
# zb.passive: 0=none, 1=points_x1.2, 2=powerup_x1.5
# zb.ability: 0=none, 1=coward, 2=guardian
# Ability cooldown (0 = ready, 1+ = on cooldown in rounds remaining)
scoreboard objectives add {ns}.zb.passive dummy
scoreboard objectives add {ns}.zb.ability dummy
scoreboard objectives add {ns}.zb.ability_cd dummy

# Spawn point group_id scoreboard
scoreboard objectives add {ns}.zb.spawn.gid dummy

# Spawn point unique id: held by spawn markers, and by zombies as "last spawn point used"
# (initial spawn or stuck-rescue) so a rescue never reuses the previous spawn point.
scoreboard objectives add {ns}.zb.spawn.sid dummy

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
		write_versioned_function("zombies/start", f"""
# Prevent starting if already active or preparing
{game_start_guards(ns, "zombies", "Zombies game")}

# Require at least one opted-in player (players are independent until added via Manage Players / + Join)
execute unless entity @a[scores={{{ns}.zb.in_game=1}}] run return run tellraw @s [{MGS_TAG},{{"text":"No players have joined the zombies game — use Manage Players first.","color":"red"}}]

{mode_start_map_bootstrap_lines(ns, "zombies", False)}

# Create zombies team
team add {ns}.zombies
team modify {ns}.zombies color yellow
team modify {ns}.zombies friendlyFire false
team modify {ns}.zombies nametagVisibility hideForOtherTeams

# Reset scores (in_game is left untouched: it's the opt-in flag, set via Manage Players / + Join)
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

# Assign opted-in players to the zombies team
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
		write_versioned_function("zombies/prep_tick", """
# Nothing to process during prep (perk selection is instant via chat click)
""")

		## End Prep → Start Round 1
		write_versioned_function("zombies/end_prep", f"""
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

		write_versioned_function("zombies/game_tick", f"""
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
execute if score #zb_has_bounds {ns}.data matches 1 as @e[type=player,scores={{{ns}.zb.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/zombies/check_bounds_player

# Check round completion
execute store result score #zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]
# Dogs still telegraphing aren't entities yet, so #zb_alive can't see them. #zb_dog_pending is only
# a fast gate though: whenever it claims dogs are pending, resync it from the real portal count so a
# desynced counter can't freeze the run. That scan only runs on the tick the round would complete.
execute if score #zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 if score #zb_dog_pending {ns}.data matches 1.. store result score #zb_dog_pending {ns}.data if entity @e[tag={ns}.dog_portal]
execute if score #zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 if score #zb_dog_pending {ns}.data matches ..0 run function {ns}:v{version}/zombies/round_complete

# Check game over: only trigger when no healthy AND no downed players remain
# - Healthy: downed=0, gamemode=!spectator (playing normally)
# - Downed: downed=1, gamemode=spectator (spectating their mannequin, can be revived)
# - Bled out: downed=0, gamemode=spectator (waiting for next round — truly dead)
execute if score #zb_round_grace {ns}.data matches 1.. run scoreboard players remove #zb_round_grace {ns}.data 1
execute unless score #zb_round_grace {ns}.data matches 1.. store result score #zb_alive_players {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]
execute unless score #zb_round_grace {ns}.data matches 1.. store result score #zb_downed_alive {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=1}},gamemode=spectator]
execute unless score #zb_round_grace {ns}.data matches 1.. run scoreboard players operation #zb_alive_players {ns}.data += #zb_downed_alive {ns}.data
execute unless score #zb_round_grace {ns}.data matches 1.. if score #zb_alive_players {ns}.data matches 0 run function {ns}:v{version}/zombies/game_over

# Stuck zombie check (every 20 ticks, 24 random non-rising zombies; escorted ones are NoAI
# and already being rescued by their trader — see escort.py)
execute store result score #zb_tick_mod {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #zb_tick_mod {ns}.data %= #20 {ns}.data
execute if score #zb_tick_mod {ns}.data matches 0 as @e[tag={ns}.zombie_round,tag=!{ns}.zb_rising,tag=!{ns}.zb_escorted,limit=24,sort=random] at @s run function {ns}:v{version}/zombies/stuck_zombie_check

# Stuck zombie glow: count up once all spawns are done (60s = 1200 ticks after last spawn)
execute if score #zb_to_spawn {ns}.data matches 0 run scoreboard players add #zb_stuck_timer {ns}.data 1
execute if score #zb_to_spawn {ns}.data matches 1.. run scoreboard players set #zb_stuck_timer {ns}.data 0
# Once threshold reached, tick glow refresh timer (every 5s = 100 ticks → apply glowing for 6s = 120 ticks)
execute if score #zb_stuck_timer {ns}.data matches 1200.. run scoreboard players add #zb_glow_timer {ns}.data 1
execute if score #zb_glow_timer {ns}.data matches 100.. run scoreboard players set #zb_glow_timer {ns}.data 0
execute if score #zb_stuck_timer {ns}.data matches 1200.. if score #zb_glow_timer {ns}.data matches 0 if score #zb_alive {ns}.data matches 1.. run function {ns}:v{version}/zombies/glow_stuck_zombies

# Last-zombies fast path: once every zombie has spawned and only a handful remain, don't make
# players wait the full 60s before stragglers glow — glow them immediately (every 100t) so a
# single hard-to-find zombie can't drag the round out (common complaint from ~round 10 on).
execute unless score #zb_alive {ns}.data matches 1..3 run scoreboard players set #zb_fewleft_timer {ns}.data 0
execute if score #zb_to_spawn {ns}.data matches 0 if score #zb_alive {ns}.data matches 1..3 run scoreboard players add #zb_fewleft_timer {ns}.data 1
execute if score #zb_fewleft_timer {ns}.data matches 1 run function {ns}:v{version}/zombies/glow_stuck_zombies
execute if score #zb_fewleft_timer {ns}.data matches 100.. run scoreboard players set #zb_fewleft_timer {ns}.data 0

# Refresh sidebar every 5 ticks.
scoreboard players add #zb_sidebar_timer {ns}.data 1
execute if score #zb_sidebar_timer {ns}.data matches 5.. run scoreboard players set #zb_sidebar_timer {ns}.data 0
execute if score #zb_sidebar_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/refresh_sidebar

# Cleanup
kill @e[type=experience_orb]
""")


		# Death & Respawn ───────────────────────────────────────────
		## On Respawn (zombies death handling → enter downed state)
		write_versioned_function("zombies/on_respawn", f"""
# Reset death counter
scoreboard players set @s {ns}.mp.death_count 0

# Increment "down count
scoreboard players add @s {ns}.zb.downs 1

# Enter downed state (revive system)
function {ns}:v{version}/zombies/revive/on_down
""")

		## Add player tick hook for zombies death detection
		write_versioned_function("player/tick", f"""
# Zombies: detect respawn
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/zombies/on_respawn
""")

		# Game Over ─────────────────────────────────────────────────

		zb_stat_line: str = (
			'tellraw @a ["","  ","🎖 ",{"selector":"@s"}," — Kills: ",'
			f'{{"score":{{"name":"@s","objective":"{ns}.zb.kills"}},"color":"green"}}," | Downs: ",'
			f'{{"score":{{"name":"@s","objective":"{ns}.zb.downs"}},"color":"red"}}," | Points: ",'
			f'{{"score":{{"name":"@s","objective":"{ns}.zb.points"}},"color":"gold"}}]'
		)
		zb_ranked_stats: str = write_ranked_stats_functions(
			ns, version, "zombies/announce_stats", "zb.in_game", "zb.kills", zb_stat_line
		)

		write_versioned_function("zombies/game_over", f"""
# Set state to ended
data modify storage {ns}:zombies game.state set value "ended"

# Snapshot the roster so a fast restart still works after the scheduled auto-stop clears
# {ns}.zb.in_game 5 seconds from now (see zombies/restart).
tag @a remove {ns}.zb_last_roster
tag @a[scores={{{ns}.zb.in_game=1}}] add {ns}.zb_last_roster

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 80 20
title @a[scores={{{ns}.zb.in_game=1}}] title {{"text":"GAME OVER","color":"dark_red","bold":true}}

# Calculate final round
execute store result score #final_round {ns}.data run data get storage {ns}:zombies game.round

# Performance summary
tellraw @a ["","\\n",{{"text":"═══════ GAME OVER ═══════","color":"dark_red","bold":true}}]
tellraw @a ["","  ","🧟 ",{{"text":"Final Round: ","color":"gray"}},{{"score":{{"name":"#final_round","objective":"{ns}.data"}},"color":"red","bold":true}}]

# Per-player stats, best first. The bare selector component renders the player's team colour.
{zb_ranked_stats}

tellraw @a ["",{{"text":"═════════════════════════","color":"dark_red","bold":true}},"\\n"]

# Signal game end
function #{ns}:zombies/on_game_end

# Stop all sounds and play gameover sound
stopsound @a
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/game_over ambient @s ~ ~ ~ 0.25 1.0

# Offer a one-click fast restart. suggest_command only runs at permission level 2, so it is a
# no-op for non-operators — exactly the operator-gated restart the design calls for.
tellraw @a ["",{MGS_TAG}," ",{btn("⟲ Fast Restart", f"/function {ns}:v{version}/zombies/restart", "green", "Restart with the same map, variant and players (operators only)")}]

# End game after 5 seconds
schedule function {ns}:v{version}/zombies/stop 100t
""")

		# Game Stop ─────────────────────────────────────────────────
		write_versioned_function("zombies/stop", f"""
# Various cleanup to set to lobby state
data modify storage {ns}:zombies game.state set value "lobby"
schedule clear {ns}:v{version}/zombies/end_prep
schedule clear {ns}:v{version}/zombies/start_round
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:max_health base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:entity_interaction_range base reset
effect clear @a[scores={{{ns}.zb.in_game=1}}]
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

		## Fast Restart ─────────────────────────────────────────────
		## Stop the current game and immediately start a new one with the same map, variant and roster.
		## Reachable only through /function (permission level 2), so it stays operator-only.
		write_versioned_function("zombies/restart", f"""
# Roster = players still in the game; if the auto-stop already cleared in_game, fall back to the
# snapshot game_over took. Tag them so the roster survives the stop cleanup below.
execute if entity @a[scores={{{ns}.zb.in_game=1}}] run tag @a[scores={{{ns}.zb.in_game=1}}] add {ns}.zb_restart
execute unless entity @a[scores={{{ns}.zb.in_game=1}}] run tag @a[tag={ns}.zb_last_roster] add {ns}.zb_restart
execute unless entity @a[tag={ns}.zb_restart] run return run tellraw @s [{MGS_TAG},{{"text":"Nothing to restart — no players from the last game.","color":"red"}}]

# Bail before tearing anything down if no map is selected (start would reject it anyway).
execute if data storage {ns}:zombies game{{map_id:""}} run return run function {ns}:v{version}/zombies/restart_no_map

# Cancel the pending auto-stop from game_over, then run the normal teardown.
schedule clear {ns}:v{version}/zombies/stop
function {ns}:v{version}/zombies/stop

# Re-opt the roster back in (stop set in_game 0) and start fresh — stop kept game.map_id / variant.
scoreboard players set @a[tag={ns}.zb_restart] {ns}.zb.in_game 1
tag @a[tag={ns}.zb_restart] remove {ns}.zb_restart
tellraw @a [{MGS_TAG},{{"text":"An operator restarted the game.","color":"yellow"}}]
function {ns}:v{version}/zombies/start
""")

		## Error path kept out of restart so the map-missing guard can both warn and drop the roster tag.
		write_versioned_function("zombies/restart_no_map", f"""
tag @a[tag={ns}.zb_restart] remove {ns}.zb_restart
tellraw @s [{MGS_TAG},{{"text":"No map selected — open the setup menu first.","color":"red"}}]
""")

		## Join Ongoing Zombies Game (late-joiner support)
		write_versioned_function("zombies/join_game", f"""
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
	class_menu_lines=(
		"# Zombies has no class selection: give the fixed starting loadout (knife + pistol), matching "
		"the start function\n"
		f"function {ns}:v{version}/zombies/inventory/give_starting_loadout"
	),
)}
""")

		# Kill Points ───────────────────────────────────────────────
		# Track kills via totalKillCount stat delta — catches all kill types (bullets, knife, etc.)
		write_versioned_function("zombies/check_kill_points", f"""
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
""")

		# Bullet hit points (+10 per bullet hit on a live zombie)
		write_versioned_function("zombies/on_hit_signal", f"""
# Only process if zombies game is active & If the hit target is a live round zombie
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute unless entity @s[tag={ns}.zombie_round] run return fail

# Mark this zombie as hit by a player this tick (gates power-up drops to player kills)
scoreboard players operation @s {ns}.zb.player_hit = #total_tick {ns}.data

# Award +10 bullet hit points to the shooter
scoreboard players operation @n[tag={ns}.ticking] {ns}.zb.points += #zb_points_hit {ns}.config
""", tags=[f"{ns}:signals/damage"])

		# Hook kill check into game_tick (per in-game player, non-spectator)
		write_versioned_function("zombies/game_tick", f"""
# Award kill points from totalKillCount delta
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:v{version}/zombies/check_kill_points
""")


		# Stuck Zombie Check ────────────────────────────────────────
		write_versioned_function("zombies/stuck_zombie_check", f"""
# @s = zombie_round entity (non-rising), run every 20 ticks on up to 24 random zombies
# Progress = distance bucket improved (or a player in melee range is VISIBLE). Resets the timer.
# Timeout depends on HOW the zombie is stuck:
# - hasn't moved at all: 400t (20s), only 100t (5s) once it has already been rescued
# - moved since last progress but not getting closer to a player: 300t (15s)

# Compute distance bucket to nearest alive player (4=very far, 0=adjacent)
scoreboard players set #cur_dist_bucket {ns}.data 4
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..96] run scoreboard players set #cur_dist_bucket {ns}.data 3
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..64] run scoreboard players set #cur_dist_bucket {ns}.data 2
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..32] run scoreboard players set #cur_dist_bucket {ns}.data 1
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..16] run scoreboard players set #cur_dist_bucket {ns}.data 0

# Compute current XZ position
execute store result score #cur_x {ns}.data run data get entity @s Pos[0]
execute store result score #cur_z {ns}.data run data get entity @s Pos[2]

# Detect any progress: bucket improved, OR bucket == 0 AND the nearby player is actually
# VISIBLE (real melee range). Proximity alone is not enough: a player a few blocks above or
# below through a floor kept the zombie permanently "not stuck" while it could never reach
# them — the LOS gate lets the timer run so the escort picks it up (see escort.py).
# XZ movement is NOT checked: a zombie attacking at close range stands still legitimately
scoreboard players set #stuck_progress {ns}.data 0
execute if score #cur_dist_bucket {ns}.data < @s {ns}.zb.stuck_dist run scoreboard players set #stuck_progress {ns}.data 1
scoreboard players set #zb_stuck_see {ns}.data 0
execute if score #cur_dist_bucket {ns}.data matches 0 positioned as @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..16] store result score #zb_stuck_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #zb_stuck_see {ns}.data matches 1 run scoreboard players set #stuck_progress {ns}.data 1

# During a PaP-room lure, a zombie that has reached the theatre centre is exactly where we want it
# (all players are hiding in the PaP room). Count that as progress so the stuck-rescue doesn't drag
# it back to the PaP door (see escort.py lure mode).
execute if score #zb_lure {ns}.data matches 1 if entity @e[tag={ns}.lure_center,distance=..12] run scoreboard players set #stuck_progress {ns}.data 1

# If progress: update all stored values, reset timestamp, and clear the rescued flag
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_dist = #cur_dist_bucket {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_x = #cur_x {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_z = #cur_z {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run tag @s remove {ns}.zb_rescued
execute if score #stuck_progress {ns}.data matches 1 run return 0

# No progress: pick the timeout for this stuck mode
# Moved = XZ differs from the snapshot taken at the last progress (block precision)
scoreboard players set #stuck_moved {ns}.data 0
execute unless score #cur_x {ns}.data = @s {ns}.zb.stuck_x run scoreboard players set #stuck_moved {ns}.data 1
execute unless score #cur_z {ns}.data = @s {ns}.zb.stuck_z run scoreboard players set #stuck_moved {ns}.data 1
scoreboard players set #stuck_threshold {ns}.data 400
execute if score #stuck_moved {ns}.data matches 1 run scoreboard players set #stuck_threshold {ns}.data 300
execute if score #stuck_moved {ns}.data matches 0 if entity @s[tag={ns}.zb_rescued] run scoreboard players set #stuck_threshold {ns}.data 100

# Down to the last couple of zombies: cut the stuck timeout to 5s so a single hard-to-reach zombie
# is escorted/teleported to the players quickly instead of dragging the round on (round 10+ complaint).
execute if score #zb_alive {ns}.data matches ..2 if score #stuck_threshold {ns}.data matches 101.. run scoreboard players set #stuck_threshold {ns}.data 100

# Compute elapsed ticks since last progress; respawn once the timeout is reached
scoreboard players operation #stuck_delta {ns}.data = #total_tick {ns}.data
scoreboard players operation #stuck_delta {ns}.data -= @s {ns}.zb.stuck_ticks
execute if score #stuck_delta {ns}.data >= #stuck_threshold {ns}.data run function {ns}:v{version}/zombies/on_stuck_zombie
""")

		write_versioned_function("zombies/on_stuck_zombie", f"""
# @s = stuck zombie — teleport it to a zombie spawn point near a player instead of killing it
# (keeps the horde intact and drops it back onto walkable navmesh so it can path again).

# Build the rescue pool via the shared spawn-proximity tagger (same 32 -> 64 -> any unlocked
# selection the round spawner uses). #zb_near_found is 0 iff nothing was tagged, so the teleport
# gate below needs no global @e existence scan. Dogs draw from their own markers: a zombie spawn can
# sit somewhere only a walker is meant to come from, and it may not even be inside the play bounds.
execute unless entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/tag_spawns_near_players
execute if entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/tag_special_spawns_near_players

# Never rescue to the spawn point this zombie last used (initial spawn or previous rescue),
# unless it is the only candidate left.
scoreboard players operation #zb_last_sid {ns}.data = @s {ns}.zb.spawn.sid
execute as @e[tag={ns}.zb_near] if score @s {ns}.zb.spawn.sid = #zb_last_sid {ns}.data run tag @s add {ns}.zb_near_prev
execute store result score #zb_near_alt {ns}.data if entity @e[tag={ns}.zb_near,tag=!{ns}.zb_near_prev]
execute if score #zb_near_alt {ns}.data matches 1.. run tag @e[tag={ns}.zb_near_prev] remove {ns}.zb_near
tag @e[tag={ns}.zb_near_prev] remove {ns}.zb_near_prev

# Teleport to the rescue spawn nearest the PLAYER, not the one nearest the stuck enemy. Picking
# from @s meant an enemy stranded far from everyone kept choosing the markers closest to itself,
# and the anti-reuse rule above then bounced it between the same two distant spawns indefinitely.
execute if score #zb_near_found {ns}.data matches 1.. at @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run function {ns}:v{version}/zombies/rescue_tp
# Everyone downed: no player to measure from, so fall back to the enemy's own position.
execute if score #zb_near_found {ns}.data matches 1.. unless entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run function {ns}:v{version}/zombies/rescue_tp
execute if score #zb_near_found {ns}.data matches 1.. run tag @s add {ns}.zb_rescued
tag @e[tag={ns}.zb_near] remove {ns}.zb_near

# The teleport moved the zombie somewhere new, so a past escort failure no longer applies:
# clear the flag so a future stuck timeout gets a trader again. It only needs to survive long
# enough to route the give_up -> on_stuck_zombie call past the escort router (see escort.py).
execute if score #zb_near_found {ns}.data matches 1.. run tag @s remove {ns}.zb_escort_failed

# Reset stuck tracking from the new position so it gets a fresh window
scoreboard players set @s {ns}.zb.stuck_dist 4
execute store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
""")

		## @s = the stuck enemy, execution POSITION = the player it should end up near (see caller).
		## Both selectors resolve from that position, so they agree on which marker was chosen.
		write_versioned_function("zombies/rescue_tp", f"""
tp @s @n[tag={ns}.zb_near]
scoreboard players operation @s {ns}.zb.spawn.sid = @n[tag={ns}.zb_near] {ns}.zb.spawn.sid
""")

		## Player boundary check (zombies): unlike zombies (out_of_world damage -> down + mannequin),
		## a player leaving the play area is a TOTAL elimination with no mannequin, respawning at the
		## next round end. Uses the same #bound_* scores loaded by shared/load_bounds.
		write_versioned_function("zombies/check_bounds_player", f"""
data modify storage {ns}:temp _player_pos set from entity @s Pos
execute store result score @s {ns}.mp.bx run data get storage {ns}:temp _player_pos[0]
execute store result score @s {ns}.mp.by run data get storage {ns}:temp _player_pos[1]
execute store result score @s {ns}.mp.bz run data get storage {ns}:temp _player_pos[2]

execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
""")

		# Spawn Point Markers ───────────────────────────────────────

		write_versioned_function("zombies/summon_spawns", f"""
# Reset the unique spawn id counter (each summoned marker gets the next id)
scoreboard players set #zb_spawn_sid {ns}.data 0

# Player spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.players
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_zb_player"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter

# Zombie spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.zombies
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_zb"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter

# Special spawns (dog rounds today, mini-bosses later). Same plumbing as zombie spawns — group_id
# gating, activation boxes, unique spawn ids — only the tag differs.
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.special
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_special"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter

# Read off the map data, not an entity scan, so start_round can gate dog rounds on a score
execute store success score #zb_has_special {ns}.data if data storage {ns}:zombies game.map.spawning_points.special[0]

# Both flags must exist before the first tick: game_tick and round completion gate on them
scoreboard players set #zb_dog_round {ns}.data 0
scoreboard players set #zb_dog_pending {ns}.data 0

# Tag group 0 spawns as unlocked (starting area)
scoreboard players set #unlock_gid {ns}.data 0
execute as @e[tag={ns}.spawn_point] if score @s {ns}.zb.spawn.gid = #unlock_gid {ns}.data run tag @s add {ns}.spawn_unlocked
""")

		write_versioned_function("zombies/summon_spawn_iter", f"""
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

# Assign a unique spawn id (lets zombies remember their previous spawn point and never reuse it)
scoreboard players add #zb_spawn_sid {ns}.data 1
scoreboard players operation @n[tag={ns}.new_spawn] {ns}.zb.spawn.sid = #zb_spawn_sid {ns}.data

# Optional activation box (zombie spawns only): store the ABSOLUTE box on the marker so the
# round spawner can gate this spawn on a player standing inside it. Only present when the map
# data defines all 6 elements [x,y,z,dx,dy,dz] (relative to this spawn).
execute if data storage {ns}:temp _spawn_iter[0].activation_box[5] run function {ns}:v{version}/zombies/store_spawn_abox

tag @n[tag={ns}.new_spawn] remove {ns}.new_spawn

data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter
""")

		## Store the absolute activation box {x,y,z,dx,dy,dz} on the just-summoned spawn marker.
		## #sx/#sy/#sz hold the marker's absolute coords; activation_box[0..2] are the relative
		## corner offset and [3..5] the box size (all in blocks).
		write_versioned_function("zombies/store_spawn_abox", f"""
execute store result score #abx {ns}.data run data get storage {ns}:temp _spawn_iter[0].activation_box[0]
execute store result score #aby {ns}.data run data get storage {ns}:temp _spawn_iter[0].activation_box[1]
execute store result score #abz {ns}.data run data get storage {ns}:temp _spawn_iter[0].activation_box[2]
scoreboard players operation #abx {ns}.data += #sx {ns}.data
scoreboard players operation #aby {ns}.data += #sy {ns}.data
scoreboard players operation #abz {ns}.data += #sz {ns}.data
execute store result storage {ns}:temp _abox.x double 1 run scoreboard players get #abx {ns}.data
execute store result storage {ns}:temp _abox.y double 1 run scoreboard players get #aby {ns}.data
execute store result storage {ns}:temp _abox.z double 1 run scoreboard players get #abz {ns}.data
execute store result storage {ns}:temp _abox.dx double 1 run data get storage {ns}:temp _spawn_iter[0].activation_box[3]
execute store result storage {ns}:temp _abox.dy double 1 run data get storage {ns}:temp _spawn_iter[0].activation_box[4]
execute store result storage {ns}:temp _abox.dz double 1 run data get storage {ns}:temp _spawn_iter[0].activation_box[5]
data modify entity @n[tag={ns}.new_spawn] data.abox set from storage {ns}:temp _abox
""")

		self.write_summon_spawn_at(extra_spawn_tags=("new_spawn",))

		# Smart Spawn Selection ─────────────────────────────────────

		write_versioned_function("zombies/tp_all_to_spawns", f"""
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/pick_spawn
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

		write_versioned_function("zombies/pick_spawn", f"""
tag @s add {ns}.spawn_pending

# Tag candidate spawns (unlocked, exclude used). Capture via command success whether any marker
# was tagged, so the "all used" fallback can branch on a score instead of a global @e scan.
execute store success score #has_candidate {ns}.data run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked,tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# If all used, re-tag all unlocked
execute if score #has_candidate {ns}.data matches 0 run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate

# Pick random candidate
execute as @n[tag={ns}.spawn_candidate,sort=random] run function {ns}:v{version}/zombies/tp_to_spawn

# Cleanup
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
""")

		write_versioned_function("zombies/tp_to_spawn", f"""
execute store result storage {ns}:temp _tp.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _tp.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _tp.z double 1 run data get entity @s Pos[2]
data modify storage {ns}:temp _tp.yaw set from entity @s data.yaw

execute as @p[tag={ns}.spawn_pending] run function {ns}:v{version}/zombies/tp_player_at with storage {ns}:temp _tp

execute unless data storage {ns}:zombies game{{state:"active"}} run tag @s add {ns}.spawn_used
""")

		self.write_tp_player_at()

		## Respawn TP for zombies
		write_versioned_function("zombies/respawn_tp", f"""
execute if entity @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player] run function {ns}:v{version}/zombies/pick_spawn
""")

		# Sidebar HUD ───────────────────────────────────────────────
		write_versioned_function("zombies/create_sidebar", f"""
scoreboard objectives add {ns}.zb_sidebar dummy

# Seed the displayed round to the upcoming round (game.round + 1) so the sidebar
# shows "Round 1" immediately during prep instead of a stale value until start_round runs
execute store result score #zb_round {ns}.data run data get storage {ns}:zombies game.round
scoreboard players add #zb_round {ns}.data 1

# Prep context: game_tick isn't maintaining #zb_alive yet (and a previous game may have left a
# stale value), so seed it once here before the (now rescan-free) refresh_sidebar.
execute store result score #zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]

function {ns}:v{version}/zombies/refresh_sidebar
scoreboard objectives setdisplay sidebar {ns}.zb_sidebar
""")

		write_versioned_function("zombies/refresh_sidebar", f"""
# Zombie count (#zb_alive) is recomputed every tick by game_tick.
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
		write_versioned_function("zombies/sidebar_rank_players", sidebar_rank_code)

		write_versioned_function("zombies/build_sidebar", f"""
scoreboard players reset * {ns}.zb_sidebar
$function #bs.sidebar:create {{objective:"{ns}.zb_sidebar",display_name:{{text:"Zombies",color:"dark_green",bold:true}},contents:$(zb_sb)}}
""")

		# Block shooting during prep
		write_versioned_function("player/right_click", f"""
# Block shooting during zombies prep phase
execute if score @s {ns}.zb.in_game matches 1 if data storage {ns}:zombies game{{state:"preparing"}} run return run scoreboard players set @s {ns}.pending_clicks 0
""", prepend=True)


def generate_zombies_game() -> None:
	""" Module-level entry (preserved signature); delegates to :class:`ZombiesMode`. """
	ZombiesMode()()


