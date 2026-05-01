
# ruff: noqa: E501
# Power-up System
# Drops from zombies via a score-threshold gate (players' combined points vs. a rising threshold)
# with a secondary 2% per-kill RNG check. Up to 4 drops per round.
# Visual: item_display + text_display. Pickup by proximity (1.5 blocks). 26.5s lifetime.
from stewbeet import LootTable, Mem, set_json_encoder, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from .perks import PERK_DEFINITIONS

# (id, placeholder_item, display_name, color, type_number)
POWERUP_TYPES: list[tuple[str, str, str, str, int]] = [
	("max_ammo",       "minecraft:amethyst_shard",       "Max Ammo",        "aqua",         1),
	("insta_kill",     "minecraft:fermented_spider_eye",  "Insta Kill",     "red",          2),
	("double_points",  "minecraft:gold_ingot",            "Double Points",  "gold",         3),
	("carpenter",      "minecraft:oak_log",               "Carpenter",      "green",        4),
	("unlimited_ammo", "minecraft:blaze_rod",             "Unlimited Ammo", "yellow",       5),
	("nuke",           "minecraft:tnt",                   "Nuke",           "red",          6),
	("random_perk",    "minecraft:glass_bottle",          "Random Perk",    "light_purple", 7),
	("free_pap",       "minecraft:diamond",               "Free PAP",       "aqua",         8),
	("cash_drop",      "minecraft:emerald",               "Cash Drop",      "green",        9),
]

POWERUP_LIFETIME: int = 530     # 26.5 seconds in ticks
POWERUP_BLINK_START: int = 200  # Blink warning when this many ticks remain (~10s)


def generate_powerups() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	perk_ids: list[str] = list(PERK_DEFINITIONS.keys())
	num_perks: int = len(perk_ids)

	# ──────────────────────────────────────────────────────────────────────────
	# Scoreboards
	# ──────────────────────────────────────────────────────────────────────────
	write_load_file(f"""
# Power-up entity scoreboards
scoreboard objectives add {ns}.zb.pu.type dummy
scoreboard objectives add {ns}.zb.pu.timer dummy

# Per-player double-points duration (ticks)
scoreboard objectives add {ns}.special.double_points dummy
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Loot table: equal-weight 9-entry pool, each entry tags the item type
	# ──────────────────────────────────────────────────────────────────────────
	Mem.ctx.data[ns].loot_tables["zombies/powerup_drop"] = set_json_encoder(LootTable({
		"pools": [{
			"rolls": 1,
			"entries": [
				{
					"type": "minecraft:item",
					"name": item,
					"weight": 1,
					"functions": [{
						"function": "minecraft:set_components",
						"components": {
							"minecraft:custom_data": {ns: {"powerup": {"type": pu_id}}},
						},
					}],
				}
				for pu_id, item, _, _, _ in POWERUP_TYPES
			],
		}],
	}))

	# ──────────────────────────────────────────────────────────────────────────
	# Drop check — called from on_zombie_dying after position is stored
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/powerups/check_drop", f"""
# Compute combined score of all in-game players
scoreboard players set #zb_total_score {ns}.data 0
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run scoreboard players operation #zb_total_score {ns}.data += @s {ns}.zb.points

# Guard: max 4 drops per round
execute if score #zb_drops_this_round {ns}.data matches 4.. run return 0

# Guard: combined score must meet threshold
execute unless score #zb_total_score {ns}.data >= #zb_score_to_drop {ns}.data run return 0

# Guard: 2% RNG check
execute store result score #pu_rng_roll {ns}.data run random value 1..100
execute unless score #pu_rng_roll {ns}.data matches 1..20 run return 0

# All checks passed: draw next type from the shuffle bag (no repeats until all 9 used)
function {ns}:v{version}/zombies/powerups/queue_draw

# Spawn visuals at the pre-stored zombie death position
data modify storage {ns}:temp _pu_spawn set value {{x:0,y:0,z:0}}
data modify storage {ns}:temp _pu_spawn.x set from entity @s Pos[0]
data modify storage {ns}:temp _pu_spawn.y set from entity @s Pos[1]
data modify storage {ns}:temp _pu_spawn.z set from entity @s Pos[2]
function {ns}:v{version}/zombies/powerups/do_spawn_random with storage {ns}:temp _pu_spawn

# Multiply threshold by 1.14 so each subsequent drop requires more score
scoreboard players operation #zb_score_to_drop {ns}.data *= #114 {ns}.data
scoreboard players operation #zb_score_to_drop {ns}.data /= #100 {ns}.data

# Increment this round's drop counter
scoreboard players add #zb_drops_this_round {ns}.data 1
""")

	# Macro: dispatch to the correct spawn_type function using the pre-stored coordinates
	do_spawn_random_lines: str = "\n".join(
		f"$execute if score #pu_spawn_type {ns}.data matches {type_num} run function {ns}:v{version}/zombies/powerups/spawn_type/{pu_id} {{x:$(x),y:$(y),z:$(z)}}"
		for pu_id, _, _, _, type_num in POWERUP_TYPES
	)
	write_versioned_function("zombies/powerups/do_spawn_random", f"""
{do_spawn_random_lines}
""")

	# Shuffle-bag queue: draw one type at a time without replacement;
	# refills with all 9 types when the bag is empty.
	num_types: int = len(POWERUP_TYPES)
	queue_random_lines: str = "\n".join(
		f"execute if score #pu_q_len {ns}.data matches {i + 1} store result score #pu_q_idx {ns}.data run random value 0..{i}"
		for i in range(num_types)
	)
	write_versioned_function("zombies/powerups/queue_draw", f"""
# Get current bag size (0 = empty or unset)
execute store result score #pu_q_len {ns}.data run data get storage {ns}:data _pu_queue

# Refill if empty
execute if score #pu_q_len {ns}.data matches ..0 run function {ns}:v{version}/zombies/powerups/queue_refill
execute if score #pu_q_len {ns}.data matches ..0 run execute store result score #pu_q_len {ns}.data run data get storage {ns}:data _pu_queue

# Pick a random index within [0, size-1]
{queue_random_lines}

# Store index into temp storage for macro call, then extract and remove
execute store result storage {ns}:temp _pu_q.idx int 1 run scoreboard players get #pu_q_idx {ns}.data
function {ns}:v{version}/zombies/powerups/queue_extract with storage {ns}:temp _pu_q
""")

	write_versioned_function("zombies/powerups/queue_refill", f"""
data modify storage {ns}:data _pu_queue set value [1,2,3,4,5,6,7,8,9]
""")

	write_versioned_function("zombies/powerups/queue_extract", f"""
$execute store result score #pu_spawn_type {ns}.data run data get storage {ns}:data _pu_queue[$(idx)]
$data remove storage {ns}:data _pu_queue[$(idx)]
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Item intercept: replace loot-spawned item entity with displays.
	# Registered to common_signals so it fires the instant the item is created.
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/powerups/intercept_item", f"""
# Only handle items tagged as powerups
execute unless data entity @s Item.components."minecraft:custom_data".{ns}.powerup run return 0

# Store type string and integer spawn coordinates in temp storage
data modify storage {ns}:temp _pu_spawn.type set from entity @s Item.components."minecraft:custom_data".{ns}.powerup.type
execute store result storage {ns}:temp _pu_spawn.x int 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pu_spawn.y int 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pu_spawn.z int 1 run data get entity @s Pos[2]

# Remove the raw item entity (replaced by visual displays below)
kill @s

# Spawn the visual item_display + text_display at the stored position
function {ns}:v{version}/zombies/powerups/spawn_display with storage {ns}:temp _pu_spawn
""", tags=["common_signals:signals/on_new_item"])

	# Dispatch to per-type spawner (macro: x, y, z come from _pu_spawn storage)
	dispatch_lines: str = "\n".join(
		f'$execute if data storage {ns}:temp _pu_spawn {{{{"type":"{pu_id}"}}}} run function {ns}:v{version}/zombies/powerups/spawn_type/{pu_id} {{{{x:$(x),y:$(y),z:$(z)}}}}'
		for pu_id, _, _, _, _ in POWERUP_TYPES
	)
	write_versioned_function("zombies/powerups/spawn_display", f"""
{dispatch_lines}
""")

	# Per-type spawners (macro: x, y, z)
	for pu_id, item, display_name, color, type_num in POWERUP_TYPES:
		write_versioned_function(f"zombies/powerups/spawn_type/{pu_id}", f"""
$summon minecraft:item_display $(x) $(y) $(z) {{Tags:["{ns}.pu_item","{ns}.pu_item_new","{ns}.gm_entity"],item:{{id:"{item}",count:1,components:{{"minecraft:item_model":"{ns}:zombies/powerup/{pu_id}"}}}},item_display:"ground",billboard:"center",transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.25f,0f],scale:[0.7f,0.7f,0.7f]}}}}
scoreboard players set @n[tag={ns}.pu_item_new] {ns}.zb.pu.type {type_num}
scoreboard players set @n[tag={ns}.pu_item_new] {ns}.zb.pu.timer {POWERUP_LIFETIME}
tag @n[tag={ns}.pu_item_new] remove {ns}.pu_item_new
$execute positioned $(x) $(y) $(z) run summon minecraft:text_display ~ ~1.0 ~ {{Tags:["{ns}.pu_text","{ns}.gm_entity"],text:{{"text":"{display_name}","color":"{color}","bold":true}},billboard:"center",background:0,shadow:true,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.5f,1.5f,1.5f]}}}}
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{{"text":"{display_name}","color":"{color}","bold":true}},{{"text":" has dropped!","color":"white"}}]
playsound minecraft:entity.experience_orb.pickup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 0.7
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Entity tick: lifetime, blink, pickup detection
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/powerups/entity_tick", f"""
# Decrement lifetime timer
scoreboard players remove @s {ns}.zb.pu.timer 1

# Expired: remove visuals and stop processing this entity
execute if score @s {ns}.zb.pu.timer matches ..0 run return run function {ns}:v{version}/zombies/powerups/expire

# Blink warning in the last {POWERUP_BLINK_START // 20} seconds
execute if score @s {ns}.zb.pu.timer matches 1..{POWERUP_BLINK_START - 1} run function {ns}:v{version}/zombies/powerups/blink_tick

# Pickup check (do_pickup kills @s, so this must be the last command)
execute if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5,tag=!{ns}.pu_collecting] run function {ns}:v{version}/zombies/powerups/do_pickup
""")

	write_versioned_function("zombies/powerups/expire", f"""
kill @e[tag={ns}.pu_text,distance=..3]
kill @s
""")

	write_versioned_function("zombies/powerups/blink_tick", f"""
# Toggle visibility every ~5 ticks using global blink state (managed in game_tick)
execute if score #zb_blink_state {ns}.data matches 0 run data merge entity @s {{view_range:0.0f}}
execute if score #zb_blink_state {ns}.data matches 1 run data merge entity @s {{view_range:64.0f}}
execute if score #zb_blink_state {ns}.data matches 0 as @e[tag={ns}.pu_text,distance=..3] run data merge entity @s {{view_range:0.0f}}
execute if score #zb_blink_state {ns}.data matches 1 as @e[tag={ns}.pu_text,distance=..3] run data merge entity @s {{view_range:64.0f}}
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Pickup
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/powerups/do_pickup", f"""
# Tag the nearest eligible player as the collector for this activation
tag @p[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5,tag=!{ns}.pu_collecting] add {ns}.pu_collecting

# Store power-up type before killing the entity
scoreboard players operation #pu_type_pickup {ns}.data = @s {ns}.zb.pu.type

# Kill the text display first (we still have a valid position)
kill @e[tag={ns}.pu_text,distance=..3]

# Activate the power-up effect (collector tag is still active here)
function {ns}:v{version}/zombies/powerups/dispatch_activate

# Kill this item_display entity
kill @s

# Clean up the collector tag so other pickups can proceed
tag @a[tag={ns}.pu_collecting] remove {ns}.pu_collecting
""")

	# Dispatch to the appropriate activation function by type number
	dispatch_activate_lines: str = "\n".join(
		f"execute if score #pu_type_pickup {ns}.data matches {type_num} run function {ns}:v{version}/zombies/powerups/activate/{pu_id}"
		for pu_id, _, _, _, type_num in POWERUP_TYPES
	)
	write_versioned_function("zombies/powerups/dispatch_activate", f"""
{dispatch_activate_lines}
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Activation functions (9 power-ups)
	# ──────────────────────────────────────────────────────────────────────────

	## 1. Max Ammo
	write_versioned_function("zombies/powerups/activate/max_ammo", f"""
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:zombies/bonus/max_ammo
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Max Ammo!","color":"aqua","bold":true}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	## 2. Insta Kill
	write_versioned_function("zombies/powerups/activate/insta_kill", f"""
scoreboard players set @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] {ns}.special.instant_kill 600
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Insta Kill!","color":"red","bold":true}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	## 3. Double Points
	write_versioned_function("zombies/powerups/activate/double_points", f"""
scoreboard players set @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] {ns}.special.double_points 600
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Double Points!","color":"gold","bold":true}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	## 4. Carpenter (instant barrier repair)
	write_versioned_function("zombies/powerups/activate/carpenter", f"""
function {ns}:v{version}/zombies/barriers/repair_all
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Carpenter!","color":"green","bold":true}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	## 5. Unlimited Ammo
	write_versioned_function("zombies/powerups/activate/unlimited_ammo", f"""
scoreboard players set @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] {ns}.special.infinite_ammo 600
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Unlimited Ammo!","color":"yellow","bold":true}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	## 6. Nuke
	write_versioned_function("zombies/powerups/activate/nuke", f"""
execute as @a[tag={ns}.pu_collecting,scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:zombies/bonus/nuke
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Nuke!","color":"red","bold":true}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 0.5
""")

	## 7. Random Perk
	# Count available (unowned) perks for the collecting player, bail early if all owned.
	# Then pick a random starting index and walk through the list to find the first unowned perk.
	count_unowned_lines: str = "\n".join(
		f"execute if score @p[tag={ns}.pu_collecting] {ns}.zb.perk.{perk_id} matches 0 run scoreboard players add #pu_perk_avail {ns}.data 1"
		for perk_id in perk_ids
	)
	iter_dispatch_lines: str = ""
	for i, perk_id in enumerate(perk_ids):
		iter_dispatch_lines += f"execute if score #pu_perk_roll {ns}.data matches {i} run function {ns}:v{version}/zombies/powerups/try_perk/{perk_id}\n"
		iter_dispatch_lines += f"execute if score #pu_perk_applied {ns}.data matches 1 run return 0\n"

	write_versioned_function("zombies/powerups/activate/random_perk", f"""
# Count unowned perks (bail early if all owned — prevents unnecessary iteration)
scoreboard players set #pu_perk_avail {ns}.data 0
{count_unowned_lines}
execute if score #pu_perk_avail {ns}.data matches 0 run return run tellraw @p[tag={ns}.pu_collecting] [{MGS_TAG},{{"text":"You already own every perk!","color":"yellow"}}]

# Pick a random starting index and walk through the list to find an unowned perk
execute store result score #pu_perk_roll {ns}.data run random value 0..{num_perks - 1}
scoreboard players set #pu_perk_applied {ns}.data 0
scoreboard players set #pu_perk_tries {ns}.data 0
function {ns}:v{version}/zombies/powerups/random_perk_iter

# Announce if a perk was successfully granted
execute if score #pu_perk_applied {ns}.data matches 1 run tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Random Perk dropped for ","color":"light_purple"}},{{"selector":"@p[tag={ns}.pu_collecting]","color":"light_purple","bold":true}},{{"text":"!","color":"light_purple"}}]
execute if score #pu_perk_applied {ns}.data matches 1 run playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	write_versioned_function("zombies/powerups/random_perk_iter", f"""
# Safety counter: prevent infinite recursion (max {num_perks + 1} iterations)
scoreboard players add #pu_perk_tries {ns}.data 1
execute if score #pu_perk_tries {ns}.data matches {num_perks + 1}.. run return 0

# Stop if a perk has already been applied in a previous iteration
execute if score #pu_perk_applied {ns}.data matches 1 run return 0

# Try the perk at the current roll index; each try_perk function sets #pu_perk_applied on success
{iter_dispatch_lines}
# No perk applied at this index (already owned): advance roll and recurse
scoreboard players add #pu_perk_roll {ns}.data 1
execute if score #pu_perk_roll {ns}.data matches {num_perks}.. run scoreboard players set #pu_perk_roll {ns}.data 0
function {ns}:v{version}/zombies/powerups/random_perk_iter
""")

	for perk_id in perk_ids:
		write_versioned_function(f"zombies/powerups/try_perk/{perk_id}", f"""
# Return early if the collecting player already owns this perk
execute if score @p[tag={ns}.pu_collecting] {ns}.zb.perk.{perk_id} matches 1 run return 0

# Apply the perk as the collecting player
execute as @p[tag={ns}.pu_collecting] run function {ns}:v{version}/zombies/perks/apply {{perk_id:"{perk_id}"}}

# Mark as applied so the iteration stops
scoreboard players set #pu_perk_applied {ns}.data 1
""")

	## 8. Free PAP
	write_versioned_function("zombies/powerups/activate/free_pap", f"""
execute as @p[tag={ns}.pu_collecting] run function {ns}:v{version}/zombies/pap/on_free_pap
""")

	## 9. Cash Drop: 400-1600 random points to all players; doubled if double_points active
	write_versioned_function("zombies/powerups/activate/cash_drop", f"""
# Roll 4..16 * 100 = 400..1600 points
execute store result score #pu_cash {ns}.data run random value 4..16
scoreboard players operation #pu_cash {ns}.data *= #100 {ns}.data

# Double the reward if double_points is active for the collecting player
execute if score @p[tag={ns}.pu_collecting] {ns}.special.double_points matches 1.. run scoreboard players operation #pu_cash {ns}.data *= #2 {ns}.data

# Award to all alive in-game players
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run scoreboard players operation @s {ns}.zb.points += #pu_cash {ns}.data

# Announce with amount
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Cash Drop! ","color":"green","bold":true}},{{"text":"+","color":"gold"}},{{"score":{{"name":"#pu_cash","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" points each!","color":"gold"}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Hooks into existing systems
	# ──────────────────────────────────────────────────────────────────────────

	## game_tick: run entity ticks, manage blink state, decrement double_points
	write_versioned_function("zombies/game_tick", f"""
# Power-up entity tick (lifetime countdown, blink, pickup detection)
execute as @e[tag={ns}.pu_item] at @s run function {ns}:v{version}/zombies/powerups/entity_tick

# Blink state: toggles between 0 and 1 every 5 ticks
scoreboard players add #zb_blink_counter {ns}.data 1
execute if score #zb_blink_counter {ns}.data matches 5.. run scoreboard players set #zb_blink_counter {ns}.data 0
execute if score #zb_blink_counter {ns}.data matches 0 run scoreboard players add #zb_blink_state {ns}.data 1
execute if score #zb_blink_state {ns}.data matches 2.. run scoreboard players set #zb_blink_state {ns}.data 0

# Decrement double_points duration for alive in-game players
execute as @a[scores={{{ns}.special.double_points=1..}},gamemode=!spectator] run scoreboard players remove @s {ns}.special.double_points 1
""")

	## start_round: reset drop counter + calculate new threshold from current player points
	write_versioned_function("zombies/start_round", f"""
# Reset per-round power-up drop counter
scoreboard players set #zb_drops_this_round {ns}.data 0

# Threshold = sum of all in-game player points at round start + 2000
scoreboard players set #zb_score_to_drop {ns}.data 0
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run scoreboard players operation #zb_score_to_drop {ns}.data += @s {ns}.zb.points
scoreboard players add #zb_score_to_drop {ns}.data 2000
""")

	## check_kill_points: award double points bonus on kills
	write_versioned_function("zombies/check_kill_points", f"""
# Double points bonus: award the same kill points again if active
execute if score @s {ns}.special.double_points matches 1.. run scoreboard players operation @s {ns}.zb.points += #total_kill_points {ns}.data
""")

	## on_hit_signal: award double points bonus on bullet hits
	write_versioned_function("zombies/on_hit_signal", f"""
# Double points bonus for bullet hit points
execute if score @n[tag={ns}.ticking] {ns}.special.double_points matches 1.. run scoreboard players operation @n[tag={ns}.ticking] {ns}.zb.points += #zb_points_hit {ns}.config
""")

	## stop: clean up all power-up entities and reset state
	write_versioned_function("zombies/stop", f"""
# Power-up cleanup
kill @e[tag={ns}.pu_item]
kill @e[tag={ns}.pu_text]
scoreboard players set #zb_drops_this_round {ns}.data 0
scoreboard players set #zb_score_to_drop {ns}.data 0
scoreboard players set @a {ns}.special.double_points 0
data modify storage {ns}:data _pu_queue set value []
""")

