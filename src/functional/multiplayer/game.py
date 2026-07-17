
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_tag, write_versioned_function

from ...config.catalogs import PRIMARY_WEAPONS, SECONDARY_WEAPONS
from ...config.stats import BASE_WEAPON, CAPACITY, GRENADE_TYPE, REMAINING_BULLETS
from ..core.respawn_countdown import respawn_countdown_tick_lines
from ..game_mode import GameMode
from ..helpers import (
	MGS_TAG,
	end_prep_transition_lines,
	game_start_guards,
	late_join_flow_lines,
	mode_start_map_bootstrap_lines,
	prep_freeze_lines,
	regen_disable_lines,
	regen_enable_lines,
)

# All multiplayer gamemodes (single source of truth for dispatch blocks)
GAMEMODES: list[str] = ["ffa", "tdm", "dom", "hp", "snd"]


class MultiplayerMode(GameMode):
	""" Generates the multiplayer game lifecycle (team-based modes, spawns, sidebars). """

	mode = "multiplayer"

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		def gm_dispatch(script: str, ret: bool = False) -> str:
			""" Build the per-gamemode dispatch lines for a given script (setup/cleanup/tick/on_kill). """
			run: str = "run return run" if ret else "run"
			return "\n".join(
				f'execute if data storage {ns}:multiplayer game{{gamemode:"{gm}"}} {run} function {ns}:v{version}/multiplayer/gamemodes/{gm}/{script}'
				for gm in GAMEMODES
			)

		## Scoreboards & Storage Setup
		self.load(
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

# Dropped-weapon lifetime (ticks remaining before the on-death dropped gun despawns)
scoreboard objectives add {ns}.mp.drop_timer dummy

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

# Require at least one opted-in player (players are independent until assigned via Manage Players / + Join)
execute unless entity @a[scores={{{ns}.mp.in_game=1}}] run return run tellraw @s [{MGS_TAG},{{"text":"No players have joined a team — use Manage Players first.","color":"red"}}]

{mode_start_map_bootstrap_lines(ns, "multiplayer", True)}

# Teams setup
team add {ns}.red
team modify {ns}.red color red
team modify {ns}.red friendlyFire false
team modify {ns}.red nametagVisibility hideForOtherTeams
team add {ns}.blue
team modify {ns}.blue color blue
team modify {ns}.blue friendlyFire false
team modify {ns}.blue nametagVisibility hideForOtherTeams
team add {ns}.ffa
team modify {ns}.ffa color yellow
team modify {ns}.ffa friendlyFire true
team modify {ns}.ffa nametagVisibility never

# Reset scores
scoreboard players set #red {ns}.mp.team 0
scoreboard players set #blue {ns}.mp.team 0
scoreboard players set #mp_has_boundary {ns}.data 0
scoreboard players set @a {ns}.mp.kills 0
scoreboard players set @a {ns}.mp.deaths 0
scoreboard players set @a {ns}.mp.death_count 0

# Set timer from time_limit
execute store result score #mp_timer {ns}.data run data get storage {ns}:multiplayer game.time_limit

# Assign vanilla teams to opted-in players only: FFA joins everyone; otherwise honor each player's
# chosen side (set via Manage Players), auto-assigning anyone who opted in without picking a team.
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run team join {ns}.ffa @a[scores={{{ns}.mp.in_game=1}}]
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] if score @s {ns}.mp.team matches 1 run team join {ns}.red @s
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] if score @s {ns}.mp.team matches 2 run team join {ns}.blue @s
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] unless score @s {ns}.mp.team matches 1.. run function {ns}:v{version}/multiplayer/auto_assign_team

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
{gm_dispatch("setup")}

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
{prep_freeze_lines(ns, "mp")}

# Give loadout to players who already have a class (positive = standard, negative = custom)
execute as @a[scores={{{ns}.mp.in_game=1}}] at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# For players with no class: auto-apply default custom loadout if set
# (add 0 initializes unset scores so the 'matches 0' check below can succeed)
scoreboard players add @a {ns}.mp.class 0
execute as @a[scores={{{ns}.mp.in_game=1}}] at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default

# Show class selection dialog to EVERYONE (so they can change during prep)
execute as @a[scores={{{ns}.mp.in_game=1}}] run function {ns}:v{version}/multiplayer/select_class

# Store current class for change detection during prep
execute as @a[scores={{{ns}.mp.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class

# Schedule end of prep (10 seconds = 200 ticks)
schedule function {ns}:v{version}/multiplayer/end_prep 200t

# Announce
tellraw @a ["","⚔ ",[{{"text":"","color":"gold","bold":true}},{{"text":"Preparing"}},"! "],{{"text":"Choose your class! Game starts in 10 seconds!","color":"yellow"}}]
""")

		## Game Stop
		write_versioned_function("multiplayer/stop", f"""
# Various cleanup to go back to lobby
data modify storage {ns}:multiplayer game.state set value "lobby"
schedule clear {ns}:v{version}/multiplayer/end_prep
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:jump_strength base reset
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:waypoint_receive_range base reset
effect clear @a[scores={{{ns}.mp.in_game=1}}] darkness
effect clear @a[scores={{{ns}.mp.in_game=1}}] blindness
effect clear @a[scores={{{ns}.mp.in_game=1}}] night_vision
gamemode adventure @a[scores={{{ns}.mp.in_game=1}},gamemode=spectator]
kill @e[tag={ns}.gm_entity]
{gm_dispatch("cleanup")}
function #{ns}:multiplayer/on_game_end

{regen_disable_lines(ns)}

# Announce scores (team scores are meaningless in FFA — the winner is announced by player_wins)
tellraw @a ["","⚔ ",[{{"text":"","color":"gold","bold":true}},{{"text":"Game Over"}},"! "]]
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} run tellraw @a ["",{{"text":"Red","color":"red"}},{{"text":": "}},{{"score":{{"name":"#red","objective":"{ns}.mp.team"}}}}," | ",{{"text":"Blue","color":"blue"}},{{"text":": "}},{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}}}}]

# Per-player match stats
execute as @a[scores={{{ns}.mp.in_game=1}}] run tellraw @a ["","  ",{{"selector":"@s","color":"yellow"}},{{"text":" ➤ ","color":"dark_gray"}},{{"score":{{"name":"@s","objective":"{ns}.mp.kills"}},"color":"green"}},{{"text":" kills","color":"gray"}},{{"text":" · ","color":"dark_gray"}},{{"score":{{"name":"@s","objective":"{ns}.mp.deaths"}},"color":"red"}},{{"text":" deaths","color":"gray"}}]

# Remove sidebar and list displays and leave teams
scoreboard objectives setdisplay sidebar
scoreboard objectives remove {ns}.sidebar
scoreboard objectives setdisplay list
team leave @a[team={ns}.red]
team leave @a[team={ns}.blue]
team leave @a[team={ns}.ffa]

# Call map leave script for each in-game player (state is still active/preparing here)
execute as @a[scores={{{ns}.mp.in_game=1}}] run function {ns}:v{version}/shared/maps/call_leave_script_at_base

scoreboard players set @a {ns}.mp.in_game 0
scoreboard players set @a {ns}.mp.team 0
scoreboard players set @a {ns}.mp.spectate_timer 0
scoreboard players set #mp_has_boundary {ns}.data 0
tag @a[tag={ns}.give_class_menu] remove {ns}.give_class_menu
""")

		## Join Ongoing Game (late-joiner support)
		write_versioned_function("multiplayer/join_game", late_join_flow_lines(
		ns,
		"multiplayer",
		f"{ns}.mp.in_game",
		"No active game to join!",
		"You are already in the game!",
		f"""
scoreboard players set @s {ns}.mp.in_game 1
scoreboard players set @s {ns}.mp.kills 0
scoreboard players set @s {ns}.mp.deaths 0
scoreboard players set @s {ns}.mp.death_count 0
scoreboard players set @s {ns}.mp.spectate_timer 0
scoreboard players set @s {ns}.last_hit 0
execute store result score @s {ns}.hp_prev run data get entity @s Health 1

# Assign to FFA team for ffa mode, otherwise auto-assign to team
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run team join {ns}.ffa @s
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} unless score @s {ns}.mp.team matches 1.. run function {ns}:v{version}/multiplayer/auto_assign_team
""",
		f"{ns}:v{version}/multiplayer/respawn_tp",
		"joined the game!",
		"yellow",
		allow_preparing=True,
		setup_extra_lines="attribute @s minecraft:waypoint_receive_range base set 0.0",
	))

		# Simulated Death ───────────────────────────────────────────
		# Called when lethal damage is intercepted (bullet/projectile) or for OOB kills
		# @s = victim player; storage mgs:input with.attacker may or may not exist

		write_versioned_function("multiplayer/simulate_death", f"""
# Ignore duplicate deaths (second bullet / OOB / vanilla death landing in the same tick as another death)
execute if score @s {ns}.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Heal to prevent actual death & Increment death stats
effect give @s instant_health 1 100 true
scoreboard players add @s {ns}.mp.deaths 1

# Fire damage signal (hit effects, hitmarker, DPS) if this came from a bullet hit
execute if data storage {ns}:input with.amount run function #{ns}:signals/damage with storage {ns}:input with

# Fire kill signal as attacker (if attacker exists in input)
execute if data storage {ns}:input with.attacker run function {ns}:v{version}/multiplayer/simulate_death_fire_kill with storage {ns}:input with

# No attacker: random funny self-death message
execute unless data storage {ns}:input with.attacker run function {ns}:v{version}/multiplayer/random_death_message

# Enter death spectate (shared with vanilla-death on_respawn)
function {ns}:v{version}/multiplayer/enter_death_spectate
""")

		## Shared death-spectate flow (@s = dying player, {ns}.temp_killer may be tagged by the caller)
		## Used by simulate_death (bullet/OOB deaths) and on_respawn (vanilla deaths)
		write_versioned_function("multiplayer/enter_death_spectate", f"""
# Drop the held gun on the ground (pickable for 30s) before anything else, while still holding it
execute at @s run function {ns}:v{version}/multiplayer/drop_held_weapon

# S&D: no respawning, mark as dead and go spectator
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run return run function {ns}:v{version}/multiplayer/gamemodes/snd/on_death

# Set player to spectator mode for 3 seconds (60 ticks)
gamemode spectator @s
scoreboard players set @s {ns}.mp.spectate_timer 60

# Spectate attacker (if tagged) or random alive player
spectate @p[tag={ns}.temp_killer,gamemode=!spectator] @s
execute unless entity @a[tag={ns}.temp_killer] run function {ns}:v{version}/multiplayer/spectate_random_player
tag @a[tag={ns}.temp_killer] remove {ns}.temp_killer

# Announce death & playsound
title @s title ["☠"]
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

		## ── On-death weapon drop ────────────────────────────────────────────────
		## Drops the gun in the player's selected weapon slot (hotbar.0/1) as a static, no-movement
		## item_display with a small interaction hitbox that other players can pick up for 30s.
		write_versioned_function("multiplayer/drop_held_weapon", f"""
# Only drop a gun held in the selected weapon slot (hotbar.0 or hotbar.1)
execute store result score #drop_sel {ns}.data run data get entity @s SelectedItemSlot
execute unless score #drop_sel {ns}.data matches 0..1 run scoreboard players set #drop_sel {ns}.data 0
execute if score #drop_sel {ns}.data matches 0 unless items entity @s hotbar.0 *[custom_data~{{{ns}:{{gun:true}}}}] run return 0
execute if score #drop_sel {ns}.data matches 1 unless items entity @s hotbar.1 *[custom_data~{{{ns}:{{gun:true}}}}] run return 0

# Capture the held gun item (strip the inventory Slot tag so it fits an item_display / item entity)
execute if score #drop_sel {ns}.data matches 0 run data modify storage {ns}:temp _dropw set from entity @s Inventory[{{Slot:0b}}]
execute if score #drop_sel {ns}.data matches 1 run data modify storage {ns}:temp _dropw set from entity @s Inventory[{{Slot:1b}}]
data remove storage {ns}:temp _dropw.Slot

# Never drop grenades
execute if data storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{GRENADE_TYPE} run return 0

# Sync live ammo into the drop (the item's custom data only refreshes a few seconds after shooting stops);
# empty guns drop with 50% of their magazine capacity instead
scoreboard players operation #drop_ammo {ns}.data = @s {ns}.{REMAINING_BULLETS}
execute store result score #drop_half {ns}.data run data get storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
scoreboard players operation #drop_half {ns}.data /= #2 {ns}.data
execute if score #drop_ammo {ns}.data matches ..0 run scoreboard players operation #drop_ammo {ns}.data = #drop_half {ns}.data
execute store result storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS} int 1 run scoreboard players get #drop_ammo {ns}.data

# Death drops carry one spare magazine at 50% capacity, embedded in the gun's custom data
# (swap drops never run this, so a swapped-away gun is not halved and carries no free magazine)
data modify storage {ns}:temp _dropmag_args set value {{}}
data modify storage {ns}:temp _dropmag_args.bw set from storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
data remove storage {ns}:temp _dropmag
function {ns}:v{version}/multiplayer/drop_mag_lookup
execute if data storage {ns}:temp _dropmag_args.mag run function {ns}:v{version}/multiplayer/drop_capture_mag with storage {ns}:temp _dropmag_args
execute if data storage {ns}:temp _dropmag run data modify storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.drop_mag set from storage {ns}:temp _dropmag

# Mid-air deaths: Bookshelf raycast straight down, the drop spawns on the first block surface below
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage {ns}:input with.piercing set value 0
data modify storage {ns}:input with.max_distance set value 100
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/empty"
data modify storage {ns}:input with.on_entry_point set value "function {ns}:v{version}/multiplayer/drop_spawn"
scoreboard players set #drop_spawned {ns}.data 0
execute rotated ~ 90 run function #bs.raycast:run with storage {ns}:input

# Nothing below within range (died over the void) -> drop at the death position
execute if score #drop_spawned {ns}.data matches 0 run function {ns}:v{version}/multiplayer/drop_spawn
""")

		## Spawn the drop entities at the current position (@s = dying player, item in {ns}:temp _dropw)
		## Called as the raycast's on_entry_point (positioned at the ground hit point) or directly as a fallback
		write_versioned_function("multiplayer/drop_spawn", f"""
scoreboard players set #drop_spawned {ns}.data 1

# Static item display lying flat on the ground (left_rotation = 90° around X), oriented by the dying player's yaw
summon minecraft:item_display ~ ~0.05 ~ {{Tags:["{ns}.mp_dropped_gun","{ns}.gm_entity","{ns}.mp_drop_new"],item_display:"ground",transformation:{{left_rotation:[0.7071068f,0f,0f,0.7071068f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.75f,0.75f,0.75f]}}}}
data modify entity @n[tag={ns}.mp_drop_new] item set from storage {ns}:temp _dropw
data modify entity @n[tag={ns}.mp_drop_new] Rotation[0] set from entity @s Rotation[0]
scoreboard players set @n[tag={ns}.mp_drop_new] {ns}.mp.drop_timer 600
tag @n[tag={ns}.mp_drop_new] remove {ns}.mp_drop_new

# Small interaction hitbox for pickup (Bookshelf right-click)
summon minecraft:interaction ~ ~ ~ {{width:0.9f,height:0.6f,response:true,Tags:["{ns}.mp_drop_int","{ns}.gm_entity","bs.entity.interaction","{ns}.mp_drop_new"]}}
scoreboard players set @n[tag={ns}.mp_drop_new] {ns}.mp.drop_timer 600
execute as @n[tag={ns}.mp_drop_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/multiplayer/pickup_dropped_weapon",executor:"source"}}
tag @n[tag={ns}.mp_drop_new] remove {ns}.mp_drop_new
""")

		## Magazine lookup: base_weapon -> magazine item id + half of one full stack for consumable ammo
		mag_lookup_lines: str = "\n".join(
			f'execute if data storage {ns}:temp _dropmag_args{{bw:"{w.item_id}"}} run '
			f'data modify storage {ns}:temp _dropmag_args merge value {{mag:"{w.magazine_id}",halfc:{max(1, w.default_mag_count // 2)}}}'
			for w in (*PRIMARY_WEAPONS, *SECONDARY_WEAPONS)
		)
		write_versioned_function("multiplayer/drop_mag_lookup", mag_lookup_lines)

		## Capture a fresh magazine from the item loot table into {ns}:temp _dropmag, filled to 50%
		write_versioned_function("multiplayer/drop_capture_mag", f"""
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.mp_mag_helper"]}}
$loot replace entity @n[tag={ns}.mp_mag_helper] contents loot {ns}:i/$(mag)
data modify storage {ns}:temp _dropmag set from entity @n[tag={ns}.mp_mag_helper] item
kill @n[tag={ns}.mp_mag_helper]
execute unless data storage {ns}:temp _dropmag run return 0

# Regular magazines: fill to 50% of their capacity (never a full magazine)
execute store result score #mag_half {ns}.data run data get storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
scoreboard players operation #mag_half {ns}.data /= #2 {ns}.data
execute if score #mag_half {ns}.data matches ..0 run scoreboard players set #mag_half {ns}.data 1
execute unless data storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.consumable store result storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS} int 1 run scoreboard players get #mag_half {ns}.data

# Consumable ammo (stack count = bullets): half of one full stack
$execute if data storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.consumable run data modify storage {ns}:temp _dropmag.count set value $(halfc)
""")

		## Pickup (Bookshelf callback, @s = clicking player)
		## Requires holding a primary/secondary gun (hotbar.0/1, grenades excluded)
		write_versioned_function("multiplayer/pickup_dropped_weapon", f"""
execute unless score @s {ns}.mp.in_game matches 1 run return fail
execute store result score #pick_sel {ns}.data run data get entity @s SelectedItemSlot
execute unless score #pick_sel {ns}.data matches 0..1 run return fail
execute unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{gun:true}}}}] run return fail
execute if data entity @s SelectedItem.components."minecraft:custom_data".{ns}.stats.{GRENADE_TYPE} run return fail
tag @s add {ns}.mp_drop_picker
execute at @e[tag=bs.interaction.target] run function {ns}:v{version}/multiplayer/pickup_collect
tag @s remove {ns}.mp_drop_picker
""")

		## Collect (@s = picker, positioned at the drop):
		## 2 guns -> swap the held gun with the drop; 1 gun -> take the drop into the free weapon slot
		write_versioned_function("multiplayer/pickup_collect", f"""
execute unless entity @n[tag={ns}.mp_dropped_gun,distance=..3] run return fail
execute store success score #pick_g0 {ns}.data if items entity @s hotbar.0 *[custom_data~{{{ns}:{{gun:true}}}}]
execute store success score #pick_g1 {ns}.data if items entity @s hotbar.1 *[custom_data~{{{ns}:{{gun:true}}}}]

# Without the Overkill perk, a pickup may not leave the player with two primary weapons
scoreboard players set #pick_deny {ns}.data 0
function {ns}:v{version}/multiplayer/pickup_overkill_check
execute if score #pick_deny {ns}.data matches 1 run return fail

# Death drops carry a spare magazine inside the gun's custom data: hand it over and strip it from the gun
execute if data entity @n[tag={ns}.mp_dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.drop_mag run function {ns}:v{version}/multiplayer/pickup_give_mag

execute if score #pick_g0 {ns}.data matches 1 if score #pick_g1 {ns}.data matches 1 run return run function {ns}:v{version}/multiplayer/pickup_swap
function {ns}:v{version}/multiplayer/pickup_take
""")

		## Primary-weapon lookup: sets #is_primary from the base_weapon string in {ns}:temp _isp.bw
		is_primary_lines: str = "\n".join(
			f'execute if data storage {ns}:temp _isp{{bw:"{w.item_id}"}} run scoreboard players set #is_primary {ns}.data 1'
			for w in PRIMARY_WEAPONS
		)
		write_versioned_function("multiplayer/is_primary_lookup", f"""
scoreboard players set #is_primary {ns}.data 0
{is_primary_lines}
""")

		## Overkill gate (@s = picker, positioned at the drop): deny when the result would be two primaries
		write_versioned_function("multiplayer/pickup_overkill_check", f"""
# Only primary drops are restricted
data modify storage {ns}:temp _isp set value {{}}
data modify storage {ns}:temp _isp.bw set from entity @n[tag={ns}.mp_dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
function {ns}:v{version}/multiplayer/is_primary_lookup
execute if score #is_primary {ns}.data matches 0 run return 0

# Overkill lets you carry two primary weapons
scoreboard players add @s {ns}.special.overkill 0
execute if score @s {ns}.special.overkill matches 1.. run return 0

# The slot that keeps its gun after this pickup: the held slot when taking, the other slot when swapping
scoreboard players operation #pick_keep {ns}.data = #pick_sel {ns}.data
execute if score #pick_g0 {ns}.data matches 1 if score #pick_g1 {ns}.data matches 1 run scoreboard players set #pick_keep {ns}.data 1
execute if score #pick_g0 {ns}.data matches 1 if score #pick_g1 {ns}.data matches 1 run scoreboard players operation #pick_keep {ns}.data -= #pick_sel {ns}.data

# If the kept gun is also a primary, deny the pickup
data modify storage {ns}:temp _isp set value {{}}
execute if score #pick_keep {ns}.data matches 0 run data modify storage {ns}:temp _isp.bw set from entity @s Inventory[{{Slot:0b}}].components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
execute if score #pick_keep {ns}.data matches 1 run data modify storage {ns}:temp _isp.bw set from entity @s Inventory[{{Slot:1b}}].components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
function {ns}:v{version}/multiplayer/is_primary_lookup
execute if score #is_primary {ns}.data matches 0 run return 0

scoreboard players set #pick_deny {ns}.data 1
tellraw @s [{MGS_TAG},{{"text":"You need the Overkill perk to carry two primary weapons.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

		## Take: only one gun owned -> the drop fills the other weapon slot, then the drop is removed
		write_versioned_function("multiplayer/pickup_take", f"""
execute if score #pick_g0 {ns}.data matches 0 run item replace entity @s hotbar.0 from entity @n[tag={ns}.mp_dropped_gun,distance=..3] contents
execute if score #pick_g0 {ns}.data matches 1 run item replace entity @s hotbar.1 from entity @n[tag={ns}.mp_dropped_gun,distance=..3] contents
playsound minecraft:entity.item.pickup player @a ~ ~ ~
kill @n[tag={ns}.mp_dropped_gun,distance=..3]
kill @e[tag=bs.interaction.target]
""")

		## Give the drop's embedded spare magazine to the picker (@s = picker, positioned at the drop)
		write_versioned_function("multiplayer/pickup_give_mag", f"""
data modify storage {ns}:temp _give set value {{}}
data modify storage {ns}:temp _give.Item set from entity @n[tag={ns}.mp_dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.drop_mag
data modify storage {ns}:temp _give.Owner set from entity @s UUID
execute at @s run function {ns}:v{version}/multiplayer/pickup_give with storage {ns}:temp _give
data remove entity @n[tag={ns}.mp_dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.drop_mag
""")

		## Zero-delay, owner-locked item entity at the picker's position
		write_versioned_function("multiplayer/pickup_give", f"""
$summon minecraft:item ~ ~0.2 ~ {{Item:$(Item),Owner:$(Owner),PickupDelay:0s,Tags:["{ns}.gm_entity"]}}
""")

		## Swap: capture the held gun, hand over the drop, then the old gun becomes the new drop (timer refreshed)
		write_versioned_function("multiplayer/pickup_swap", f"""
data modify storage {ns}:temp _swapw set from entity @s Inventory[{{Slot:0b}}]
execute if score #pick_sel {ns}.data matches 1 run data modify storage {ns}:temp _swapw set from entity @s Inventory[{{Slot:1b}}]
data remove storage {ns}:temp _swapw.Slot

# Held guns carry remaining_bullets:-1 in their item NBT (the live count is on the scoreboard), so sync it in
execute store result storage {ns}:temp _swapw.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS} int 1 run scoreboard players get @s {ns}.{REMAINING_BULLETS}

execute if score #pick_sel {ns}.data matches 0 run item replace entity @s hotbar.0 from entity @n[tag={ns}.mp_dropped_gun,distance=..3] contents
execute if score #pick_sel {ns}.data matches 1 run item replace entity @s hotbar.1 from entity @n[tag={ns}.mp_dropped_gun,distance=..3] contents
data modify entity @n[tag={ns}.mp_dropped_gun,distance=..3] item set from storage {ns}:temp _swapw
playsound minecraft:entity.item.pickup player @a ~ ~ ~
scoreboard players set @n[tag={ns}.mp_dropped_gun,distance=..3] {ns}.mp.drop_timer 600
scoreboard players set @n[tag={ns}.mp_drop_int,distance=..3] {ns}.mp.drop_timer 600
""")

		## Random death message for self-deaths (OOB, environmental)
		write_versioned_function("multiplayer/random_death_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"made a terrible mistake","color":"gray"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"forgot how gravity works","color":"gray"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"played themselves","color":"gray"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"left the battlefield","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"embraced the void","color":"gray"}}]
""")

		## Random self-kill message (grenade, RPG, own explosion)
		write_versioned_function("multiplayer/random_self_kill_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"blew themselves up","color":"gray"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"got a taste of their own medicine","color":"gray"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"found out the blast radius the hard way","color":"gray"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"didn't throw the grenade far enough","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"is their own worst enemy","color":"gray"}}]
""")

		## Random kill message (uses temp_killer/temp_victim tags, shared by simulate_death + on_respawn)
		write_versioned_function("multiplayer/random_kill_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]"}}," ",{{"text":"eliminated","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]"}}," ",{{"text":"took down","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]"}}," ",{{"text":"dispatched","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]"}}," ",{{"text":"sent","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]"}}," ",{{"text":"to the shadow realm","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]"}}," ",{{"text":"wiped","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]"}}," ",{{"text":"off the map","color":"gray"}}]
""")

		## Kill Tracking (Signal Listener) - now dispatches to gamemode
		write_versioned_function("multiplayer/on_kill_signal", f"""
# Only process if multiplayer game is active
execute unless data storage {ns}:multiplayer game{{state:"active"}} run return fail

# Dispatch to gamemode-specific kill handler
{gm_dispatch("on_kill", ret=True)}
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
$tellraw @a ["","🏆 ",{{"text":"$(team) Team Wins!","color":"gold","bold":true}}]
tellraw @a ["",[{{"text":"","color":"gray"}},"  ",{{"text":"Final Score - Red"}},": "],{{"score":{{"name":"#red","objective":"{ns}.mp.team"}},"color":"red"}},[{{"text":"","color":"gray"}}," ",{{"text":"vs Blue"}},": "],{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}},"color":"blue"}}]

# End game
function {ns}:v{version}/multiplayer/stop
""")

		# Game Tick (runs once per server tick when game is active)
		self.tick(f"""
# Multiplayer game tick
execute if data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/game_tick
execute if data storage {ns}:multiplayer game{{state:"preparing"}} run function {ns}:v{version}/multiplayer/prep_tick
""")

		write_versioned_function("multiplayer/game_tick", f"""
{respawn_countdown_tick_lines(ns, "mp", f"{ns}:v{version}/multiplayer/actual_respawn")}

# Dropped-weapon lifetime: count down and remove expired drops (display + interaction together)
execute as @e[tag={ns}.mp_dropped_gun] run scoreboard players remove @s {ns}.mp.drop_timer 1
execute as @e[tag={ns}.mp_drop_int] run scoreboard players remove @s {ns}.mp.drop_timer 1
kill @e[tag={ns}.mp_dropped_gun,scores={{{ns}.mp.drop_timer=..0}}]
kill @e[tag={ns}.mp_drop_int,scores={{{ns}.mp.drop_timer=..0}}]

# Timer
scoreboard players remove #mp_timer {ns}.data 1

# Timer display every second (20 ticks)
execute store result score #tick_mod {ns}.data run scoreboard players get #mp_timer {ns}.data
scoreboard players operation #tick_mod {ns}.data %= #20 {ns}.data
execute if score #tick_mod {ns}.data matches 0 run function {ns}:v{version}/multiplayer/timer_display

# Time's up
execute if score #mp_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/time_up

# Boundary + out-of-bounds enforcement in ONE pass over the playing-players selector (was two
# scans over the identical, multi-filter selector). Skips respawn-protected/non-playing players.
execute as @e[type=player,scores={{{ns}.mp.in_game=1,{ns}.mp.death_count=0}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/multiplayer/enforce_bounds

# Gamemode tick dispatch
{gm_dispatch("tick")}

# Tracker perk: render enemy footprints to perked players (every 6 ticks)
execute store result score #tick_mod {ns}.data run scoreboard players get #mp_timer {ns}.data
scoreboard players operation #tick_mod {ns}.data %= #6 {ns}.data
execute if score #tick_mod {ns}.data matches 0 if entity @a[scores={{{ns}.mp.in_game=1,{ns}.special.tracker=1..}}] run function {ns}:v{version}/multiplayer/perks/tracker_tick

# Call map-defined tick script
function {ns}:v{version}/shared/maps/call_tick_script_at_base
""")

		## perks/tracker_tick - One pass over all live players: drop a footprint at each one's feet
		write_versioned_function("multiplayer/perks/tracker_tick", f"""
execute as @a[scores={{{ns}.mp.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/multiplayer/perks/tracker_footprint
""")

		## perks/tracker_footprint - @s = the tracked player (at their position);
		## the footprint is forced to enemy Tracker holders only, via a single team-filtered selector.
		## (Team modes: opposite team. FFA/team 0: every other Tracker holder, excluded via distance.)
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

		## Per-player boundary + OOB enforcement (one scan in game_tick dispatches this). @s = a playing
		## player. Merges the former two separate game_tick passes over the same selector.
		write_versioned_function("multiplayer/enforce_bounds", f"""
# Coordinate bounds (only when the map defines a boundary box). May eliminate @s -> spectator.
execute if score #mp_has_boundary {ns}.data matches 1 run function {ns}:v{version}/multiplayer/check_bounds

# OOB markers. Skip if the coordinate check just eliminated @s this tick (now a spectator) — the
# original two-pass form excluded such players via its gamemode=!spectator selector, so doing the
# OOB kill here too would double-count the death.
execute if entity @s[gamemode=!spectator] if entity @e[tag={ns}.oob_point,distance=..5] run function {ns}:v{version}/multiplayer/bounds_kill
""")

		## Environmental kill: out of boundaries or near an OOB marker (simulate death, never /kill)
		write_versioned_function("multiplayer/bounds_kill", f"""
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

		self.write_summon_spawn_at()

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

# Tag candidate spawn markers of the right type (exclude already-used spawns). #mp_cand_count
# tracks how many candidates currently carry the tag, so the "all contested" fallback below can
# branch on a score instead of a global @e existence scan. Seed it with the count just tagged.
$execute store result score #mp_cand_count {ns}.data run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_$(type),tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# Remove candidates that have an enemy player within 5 blocks (each removal decrements the count)
execute as @e[tag={ns}.spawn_candidate] at @s if entity @a[tag={ns}.spawn_enemy,distance=..5] run function {ns}:v{version}/multiplayer/uncontest_spawn

# If all were removed (all spawns used or contested), re-tag all as candidates
$execute if score #mp_cand_count {ns}.data matches 0 run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_$(type)] add {ns}.spawn_candidate

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

		## Drop a contested candidate marker and keep #mp_cand_count in sync (@s = the spawn marker).
		## The tag is always present here (we only iterate spawn_candidate markers), so the decrement
		## is exactly 1:1 with a removal — letting pick_spawn's fallback test a score, not scan @e.
		write_versioned_function("multiplayer/uncontest_spawn", f"""
tag @s remove {ns}.spawn_candidate
scoreboard players remove #mp_cand_count {ns}.data 1
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
		self.write_tp_player_at()

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
			f'[" ⏱ ",'
			f'[{{score:{{name:"#timer_min",objective:"{ns}.data"}},"color":"yellow"}},'
			f'{{text:":"}},'
			f'{{score:{{name:"#timer_tens",objective:"{ns}.data"}}}},'
			f'{{score:{{name:"#timer_ones",objective:"{ns}.data"}}}}]]'
		)
		sb_red = f'[["", " 🔴 ",{{text:"Red",color:"red"}}],[" ",{{score:{{name:"#red",objective:"{ns}.mp.team"}},color:"white"}}]]'
		sb_blue = f'[["", " 🔵 ",{{text:"Blue",color:"blue"}}],[" ",{{score:{{name:"#blue",objective:"{ns}.mp.team"}},color:"white"}}]]'
		sb_limit = f'[{{text:" First to ",color:"gray"}},{{score:{{name:"#score_limit",objective:"{ns}.data"}},color:"white"}}]'
		sb_spacer = '" "'

		## Team sidebar (TDM/SND) — takes $(title) macro arg
		write_versioned_function("multiplayer/create_sidebar_team", f"""
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"$(title)",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

		## FFA sidebar — ranked players with kills using bs.sidebar
		write_versioned_function("multiplayer/create_sidebar_ffa", f"""
function {ns}:v{version}/multiplayer/refresh_sidebar_ffa
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
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Free For All",color:"gold",bold:true}},contents:$(ffa_sb)}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
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
execute if score #dom_owner_a {ns}.data matches 0 run data modify storage {ns}:temp dom_sb.a set value '[" ",{{"text":"A: ","color":"gray"}},"⚪ ",{{"text":"Neutral","color":"gray"}}]'
execute if score #dom_owner_a {ns}.data matches 1 run data modify storage {ns}:temp dom_sb.a set value '[" ",{{"text":"A: ","color":"red"}},"🔴 ",{{"text":"Red","color":"red"}}]'
execute if score #dom_owner_a {ns}.data matches 2 run data modify storage {ns}:temp dom_sb.a set value '[" ",{{"text":"A: ","color":"blue"}},"🔵 ",{{"text":"Blue","color":"blue"}}]'

# Zone B
execute if score #dom_owner_b {ns}.data matches 0 run data modify storage {ns}:temp dom_sb.b set value '[" ",{{"text":"B: ","color":"gray"}},"⚪ ",{{"text":"Neutral","color":"gray"}}]'
execute if score #dom_owner_b {ns}.data matches 1 run data modify storage {ns}:temp dom_sb.b set value '[" ",{{"text":"B: ","color":"red"}},"🔴 ",{{"text":"Red","color":"red"}}]'
execute if score #dom_owner_b {ns}.data matches 2 run data modify storage {ns}:temp dom_sb.b set value '[" ",{{"text":"B: ","color":"blue"}},"🔵 ",{{"text":"Blue","color":"blue"}}]'

# Zone C
execute if score #dom_owner_c {ns}.data matches 0 run data modify storage {ns}:temp dom_sb.c set value '[" ",{{"text":"C: ","color":"gray"}},"⚪ ",{{"text":"Neutral","color":"gray"}}]'
execute if score #dom_owner_c {ns}.data matches 1 run data modify storage {ns}:temp dom_sb.c set value '[" ",{{"text":"C: ","color":"red"}},"🔴 ",{{"text":"Red","color":"red"}}]'
execute if score #dom_owner_c {ns}.data matches 2 run data modify storage {ns}:temp dom_sb.c set value '[" ",{{"text":"C: ","color":"blue"}},"🔵 ",{{"text":"Blue","color":"blue"}}]'

# Build sidebar with dynamic point entries
function {ns}:v{version}/multiplayer/build_sidebar_dom with storage {ns}:temp dom_sb
""")

		write_versioned_function("multiplayer/build_sidebar_dom", f"""
scoreboard players reset * {ns}.sidebar
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Domination",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},$(a),$(b),$(c),{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

		## Hardpoint sidebar — shows team scores + controlling team + time to move
		write_versioned_function("multiplayer/create_sidebar_hp", f"""
scoreboard players reset * {ns}.sidebar
function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Hardpoint",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},[{{text:" Zone: ",color:"dark_purple"}},{{score:{{name:"#hp_rotate_sec",objective:"{ns}.data"}},color:"white"}},{{text:"s left",color:"gray"}}],{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

		# Shooting Block During Prep
		## Prepend to right_click: block shooting during prep phase
		write_versioned_function("player/right_click", f"""
# Block shooting during multiplayer prep phase
execute if score @s {ns}.mp.in_game matches 1 if data storage {ns}:multiplayer game{{state:"preparing"}} run return run scoreboard players set @s {ns}.pending_clicks 0
""", prepend=True)

		# Prep Phase
		## Prep tick: during 10s warmup, detect class changes and apply immediately
		write_versioned_function("multiplayer/prep_tick", f"""
# Check for class changes and apply immediately
execute as @a[scores={{{ns}.mp.in_game=1}}] unless score @s {ns}.mp.class = @s {ns}.mp.prev_class unless score @s {ns}.mp.class matches 0 at @s run function {ns}:v{version}/multiplayer/apply_class
execute as @a[scores={{{ns}.mp.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class
""")

		## End prep: unfreeze players, transition to active
		write_versioned_function("multiplayer/end_prep", f"""
{end_prep_transition_lines(ns, "multiplayer", "mp")}

# Call map start scripts (state is now active, chunks had time to load)
function {ns}:v{version}/shared/maps/call_start_script_at_base

# Announce
tellraw @a ["","⚔ ",[{{"text":"","color":"green","bold":true}},{{"text":"GO! GO! GO!"}}]]
""")


def generate_game() -> None:
	""" Module-level entry (preserved signature); delegates to :class:`MultiplayerMode`. """
	MultiplayerMode()()


