
# ruff: noqa: E501
# Power-up System
# Drops from zombies via a score-threshold gate (players' combined points vs. a rising threshold)
# with a secondary 4% per-kill RNG check. Up to 4 drops per round.
# Visual: item entity + text_display. Pickup by proximity (1.5 blocks). 26.5s lifetime.
from stewbeet import JsonDict, LootTable, Mem, set_json_encoder, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from .perks import PERK_DEFINITIONS

# Each power-up is a dict with required keys:
#   item         - placeholder item id
#   display      - display name shown in-game
#   color        - text color
#   type_num     - integer used in scoreboards/dispatch
#   tier         - "common" | "rare"  (rare = 25% chance to appear each shuffle cycle)
#
# Timed power-ups additionally carry:
#   duration     - active duration in ticks
#   scoreboard   - the {ns}.special.<scoreboard> objective name
#   bossbar_id   - the {ns}:pu_<bossbar_id> bossbar name
#   bb_color     - bossbar color string
POWERUP_TYPES: dict[str, JsonDict] = {
	"max_ammo":       {"item": "minecraft:amethyst_shard",       "display": "Max Ammo",       "color": "aqua",         "type_num": 1, "tier": "common"},
	"insta_kill":     {"item": "minecraft:fermented_spider_eye", "display": "Insta Kill",     "color": "red",          "type_num": 2, "tier": "common", "duration": 600, "scoreboard": "instant_kill",  "bossbar_id": "pu_insta_kill",     "bb_color": "red"},
	"double_points":  {"item": "minecraft:gold_ingot",           "display": "Double Points",  "color": "yellow",       "type_num": 3, "tier": "common", "duration": 600, "scoreboard": "double_points", "bossbar_id": "pu_double_points",  "bb_color": "yellow"},
	"carpenter":      {"item": "minecraft:oak_log",              "display": "Carpenter",      "color": "gold",         "type_num": 4, "tier": "common"},
	"nuke":           {"item": "minecraft:tnt",                  "display": "Nuke",           "color": "red",          "type_num": 5, "tier": "common"},
	"unlimited_ammo": {"item": "minecraft:blaze_rod",            "display": "Unlimited Ammo", "color": "green",        "type_num": 6, "tier": "rare",   "duration": 600, "scoreboard": "infinite_ammo", "bossbar_id": "pu_unlimited_ammo", "bb_color": "green"},
	"random_perk":    {"item": "minecraft:glass_bottle",         "display": "Random Perk",    "color": "light_purple", "type_num": 7, "tier": "rare"},
	"free_pap":       {"item": "minecraft:diamond",              "display": "Free PAP",       "color": "aqua",         "type_num": 8, "tier": "rare"},
	"cash_drop":      {"item": "minecraft:emerald",              "display": "Cash Drop",      "color": "green",        "type_num": 9, "tier": "rare"},
}

POWERUP_LIFETIME: int    = 530  # 26.5 seconds in ticks
POWERUP_BLINK_START: int = 200  # Blink warning when this many ticks remain (~10s)

# Convenience view: only power-ups with a timed duration
TIMED_POWERUPS: dict[str, JsonDict] = {k: v for k, v in POWERUP_TYPES.items() if "duration" in v}


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
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Loot table: equal-weight pool, each entry tags the item type
	# ──────────────────────────────────────────────────────────────────────────
	Mem.ctx.data[ns].loot_tables["zombies/powerup_drop"] = set_json_encoder(LootTable({
		"pools": [{
			"rolls": 1,
			"entries": [
				{
					"type": "minecraft:item",
					"name": v["item"],
					"weight": 1,
					"functions": [{
						"function": "minecraft:set_components",
						"components": {
							"minecraft:custom_data": {ns: {"powerup": {"type": pu_id}}},
						},
					}],
				}
				for pu_id, v in POWERUP_TYPES.items()
			],
		}],
	}))

	# ──────────────────────────────────────────────────────────────────────────
	# Drop check — called from on_zombie_dying after position is stored
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/powerups/check_drop", f"""
# Compute combined score of all in-game players
scoreboard players set #zb_total_score {ns}.data 0
scoreboard players operation #zb_total_score {ns}.data += @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points

# Guard: max 4 drops per round
execute if score #zb_drops_this_round {ns}.data matches 4.. run return 0

# Guard: combined score must meet threshold
execute unless score #zb_total_score {ns}.data >= #zb_score_to_drop {ns}.data run return 0

# Guard: 4% RNG check
execute store result score #pu_rng_roll {ns}.data run random value 1..100
execute unless score #pu_rng_roll {ns}.data matches 1..4 run return 0

# All checks passed: draw and spawn at this entity's position
function {ns}:v{version}/zombies/powerups/spawn_random_at_self

# Multiply threshold by 1.14 so each subsequent drop requires more score
scoreboard players operation #zb_score_to_drop {ns}.data *= #114 {ns}.data
scoreboard players operation #zb_score_to_drop {ns}.data /= #100 {ns}.data

# Increment this round's drop counter
scoreboard players add #zb_drops_this_round {ns}.data 1
""")

	# Draws a random power-up from the shuffle bag and spawns it at @s's position.
	# Can be called directly (e.g. as OP) to force-spawn a power-up at your feet.
	write_versioned_function("zombies/powerups/spawn_random_at_self", f"""
# Draw next type from the shuffle bag (no repeats until the current cycle is exhausted)
function {ns}:v{version}/zombies/powerups/queue_draw

# Spawn visuals at @s's position
scoreboard players add #pu_uid {ns}.data 1
data modify storage {ns}:temp _pu_spawn set value {{x:0,y:0,z:0,uid:0}}
data modify storage {ns}:temp _pu_spawn.x set from entity @s Pos[0]
data modify storage {ns}:temp _pu_spawn.y set from entity @s Pos[1]
data modify storage {ns}:temp _pu_spawn.z set from entity @s Pos[2]
execute store result storage {ns}:temp _pu_spawn.uid int 1 run scoreboard players get #pu_uid {ns}.data
function {ns}:v{version}/zombies/powerups/do_spawn_random with storage {ns}:temp _pu_spawn
""")

	# Macro: dispatch to the correct spawn_type function using the pre-stored coordinates
	do_spawn_random_lines: str = "\n".join(
		f"$execute if score #pu_spawn_type {ns}.data matches {v['type_num']} run function {ns}:v{version}/zombies/powerups/spawn_type/{pu_id} {{x:$(x),y:$(y),z:$(z),uid:$(uid)}}"
		for pu_id, v in POWERUP_TYPES.items()
	)
	write_versioned_function("zombies/powerups/do_spawn_random", f"""
{do_spawn_random_lines}
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Shuffle-bag queue
	# ──────────────────────────────────────────────────────────────────────────
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

	queue_refill_common_lines: str = "\n".join(
		f"data modify storage {ns}:data _pu_queue append value {v['type_num']}"
		for _pu_id, v in POWERUP_TYPES.items()
		if v["tier"] == "common"
	)
	queue_refill_rare_lines: str = "\n".join(
		f"execute store result score #pu_rare_roll_{v['type_num']} {ns}.data run random value 1..100\n"
		f"execute if score #pu_rare_roll_{v['type_num']} {ns}.data matches 1..25 run data modify storage {ns}:data _pu_queue append value {v['type_num']}"
		for _pu_id, v in POWERUP_TYPES.items()
		if v["tier"] == "rare"
	)
	write_versioned_function("zombies/powerups/queue_refill", f"""
data modify storage {ns}:data _pu_queue set value []

# Always include common power-ups in every cycle
{queue_refill_common_lines}

# Each rare power-up has an independent 25% chance to join this cycle
{queue_refill_rare_lines}
""")

	write_versioned_function("zombies/powerups/queue_extract", f"""
$execute store result score #pu_spawn_type {ns}.data run data get storage {ns}:data _pu_queue[$(idx)]
$data remove storage {ns}:data _pu_queue[$(idx)]
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Item intercept: replace loot-spawned item entity with the managed power-up visuals
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/powerups/intercept_item", f"""
# Only handle items tagged as powerups
execute unless data entity @s Item.components."minecraft:custom_data".{ns}.powerup run return 0

# Store type string and integer spawn coordinates in temp storage
scoreboard players add #pu_uid {ns}.data 1
data modify storage {ns}:temp _pu_spawn.type set from entity @s Item.components."minecraft:custom_data".{ns}.powerup.type
execute store result storage {ns}:temp _pu_spawn.x int 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pu_spawn.y int 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pu_spawn.z int 1 run data get entity @s Pos[2]
execute store result storage {ns}:temp _pu_spawn.uid int 1 run scoreboard players get #pu_uid {ns}.data

# Remove the raw item entity (replaced by visual displays below)
kill @s

# Spawn the managed item entity + text_display at the stored position
function {ns}:v{version}/zombies/powerups/spawn_display with storage {ns}:temp _pu_spawn
""", tags=["common_signals:signals/on_new_item"])

	# Dispatch to per-type spawner
	dispatch_lines: str = "\n".join(
		f'$execute if data storage {ns}:temp _pu_spawn {{"type":"{pu_id}"}} run function {ns}:v{version}/zombies/powerups/spawn_type/{pu_id} {{x:$(x),y:$(y),z:$(z),uid:$(uid)}}'
		for pu_id in POWERUP_TYPES
	)
	write_versioned_function("zombies/powerups/spawn_display", f"""
{dispatch_lines}
""")

	# Per-type spawners (macro: x, y, z)
	for pu_id, v in POWERUP_TYPES.items():
		item: str = v["item"]
		display_name: str = v["display"]
		color: str = v["color"]
		type_num: int = v["type_num"]
		write_versioned_function(f"zombies/powerups/spawn_type/{pu_id}", f"""
$summon minecraft:item $(x) $(y) $(z) {{Tags:["{ns}.pu_item","{ns}.pu_item_new","{ns}.gm_entity"],PickupDelay:32767,Invulnerable:1b,Item:{{id:"{item}",count:1,components:{{"minecraft:custom_data":{{{ns}:{{powerup_uid:$(uid)}}}}}}}}}}
scoreboard players set @n[tag={ns}.pu_item_new] {ns}.zb.pu.type {type_num}
scoreboard players set @n[tag={ns}.pu_item_new] {ns}.zb.pu.timer {POWERUP_LIFETIME}
tag @n[tag={ns}.pu_item_new] remove {ns}.pu_item_new
$execute positioned $(x) $(y) $(z) run summon minecraft:text_display ~ ~1.0 ~ {{Tags:["{ns}.pu_text","{ns}.gm_entity"],text:{{"text":"{display_name}","color":"{color}","bold":true}},billboard:"vertical",background:0,shadow:true,view_range:64.0f,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.5f,1.5f,1.5f]}}}}
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
kill @n[tag={ns}.pu_text,distance=..3]
kill @s
""")

	# Blink implementation matching BO2's ~0.4s full cycle (4 ticks on, 4 ticks off).
	write_versioned_function("zombies/powerups/blink_tick", f"""
# "Off" frame: hide the item entity and the text_display
execute if score #zb_blink_state {ns}.data matches 0 run data modify entity @s Item.components."minecraft:custom_data".{ns}.powerup_model set from entity @s Item.components."minecraft:item_model"
execute if score #zb_blink_state {ns}.data matches 0 run data modify entity @s Item.components."minecraft:item_model" set value "minecraft:air"
# "On" frame: show the item entity again
execute if score #zb_blink_state {ns}.data matches 1 run data modify entity @s Item.components."minecraft:item_model" set from entity @s Item.components."minecraft:custom_data".{ns}.powerup_model
# text_display has no generic visibility tag — use view_range toggle instead
execute if score #zb_blink_state {ns}.data matches 0 as @n[tag={ns}.pu_text,distance=..3] run data merge entity @s {{view_range:0.0f}}
execute if score #zb_blink_state {ns}.data matches 1 as @n[tag={ns}.pu_text,distance=..3] run data merge entity @s {{view_range:64.0f}}
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
kill @n[tag={ns}.pu_text,distance=..3]

# Activate the power-up effect (collector tag is still active here)
function {ns}:v{version}/zombies/powerups/dispatch_activate

# Kill this power-up item entity
kill @s

# Clean up the collector tag so other pickups can proceed
tag @a[tag={ns}.pu_collecting] remove {ns}.pu_collecting
""")

	dispatch_activate_lines: str = "\n".join(
		f"execute if score #pu_type_pickup {ns}.data matches {v['type_num']} run function {ns}:v{version}/zombies/powerups/activate/{pu_id}"
		for pu_id, v in POWERUP_TYPES.items()
	)
	write_versioned_function("zombies/powerups/dispatch_activate", f"""
{dispatch_activate_lines}
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Activation functions
	# ──────────────────────────────────────────────────────────────────────────

	## 1. Max Ammo
	write_versioned_function("zombies/powerups/activate/max_ammo", f"""
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:zombies/bonus/max_ammo
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Max Ammo!","color":"aqua","bold":true}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	## 2-4. Timed power-ups: Insta Kill, Double Points, Unlimited Ammo
	# All share the same bossbar+scoreboard activation pattern, driven by TIMED_POWERUPS.
	for pu_id, v in TIMED_POWERUPS.items():
		duration: int     = v["duration"]
		scoreboard: str   = v["scoreboard"]
		bossbar_id: str   = v["bossbar_id"]
		display_name: str = v["display"]
		color: str        = v["color"]
		bb_color: str     = v["bb_color"]
		write_versioned_function(f"zombies/powerups/activate/{pu_id}", f"""
scoreboard players set @a[scores={{{ns}.zb.in_game=1}}] {ns}.special.{scoreboard} {duration}
bossbar remove {ns}:{bossbar_id}
bossbar add {ns}:{bossbar_id} {{"text":"{display_name} - {duration // 20}s","bold":true,"color":"{bb_color}"}}
bossbar set {ns}:{bossbar_id} max {duration}
bossbar set {ns}:{bossbar_id} value {duration}
bossbar set {ns}:{bossbar_id} color {bb_color}
bossbar set {ns}:{bossbar_id} style progress
bossbar set {ns}:{bossbar_id} players @a[scores={{{ns}.zb.in_game=1}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	## 5. Carpenter (instant barrier repair)
	write_versioned_function("zombies/powerups/activate/carpenter", f"""
function {ns}:v{version}/zombies/barriers/repair_all
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Carpenter!","color":"green","bold":true}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	## 6. Nuke
	write_versioned_function("zombies/powerups/activate/nuke", f"""
execute as @a[tag={ns}.pu_collecting,scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:zombies/bonus/nuke
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Nuke!","color":"red","bold":true}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 0.5
""")

	## 7. Random Perk
	count_unowned_lines: str = "\n".join(
		f"execute if score @p[tag={ns}.pu_collecting] {ns}.zb.perk.{perk_id} matches 0 run scoreboard players add #pu_perk_avail {ns}.data 1"
		for perk_id in perk_ids
	)
	iter_dispatch_lines: str = ""
	for i, perk_id in enumerate(perk_ids):
		iter_dispatch_lines += f"execute if score #pu_perk_roll {ns}.data matches {i} run function {ns}:v{version}/zombies/powerups/try_perk/{perk_id}\n"
		iter_dispatch_lines += f"execute if score #pu_perk_applied {ns}.data matches 1 run return 0\n"

	write_versioned_function("zombies/powerups/activate/random_perk", f"""
# Count unowned perks (bail early if all owned)
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

# Award to all in-game players
execute as @a[scores={{{ns}.zb.in_game=1}}] run scoreboard players operation @s {ns}.zb.points += #pu_cash {ns}.data

# Announce with amount
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Cash Drop! ","color":"green","bold":true}},{{"text":"+","color":"gold"}},{{"score":{{"name":"#pu_cash","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" points each!","color":"gold"}}]
playsound minecraft:entity.player.levelup master @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Bossbar update functions — generated from TIMED_POWERUPS, one per entry
	# ──────────────────────────────────────────────────────────────────────────
	for pu_id, v in TIMED_POWERUPS.items():
		scoreboard: str   = v["scoreboard"]
		bossbar_id: str   = v["bossbar_id"]
		display_name: str = v["display"]
		color: str        = v["color"]
		write_versioned_function(f"zombies/powerups/update_{pu_id}_bb", f"""
# Find max remaining duration across all players with active {pu_id}
scoreboard players set #pu_max_duration {ns}.data 0
scoreboard players operation #pu_max_duration {ns}.data > @a[scores={{{ns}.special.{scoreboard}=1..}}] {ns}.special.{scoreboard}

# If max duration is 0, remove bossbar; otherwise update value and name with countdown
execute if score #pu_max_duration {ns}.data matches ..0 run bossbar remove {ns}:{bossbar_id}
execute if score #pu_max_duration {ns}.data matches 1.. store result bossbar {ns}:{bossbar_id} value run scoreboard players get #pu_max_duration {ns}.data
execute if score #pu_max_duration {ns}.data matches 1.. run scoreboard players operation #pu_seconds {ns}.data = #pu_max_duration {ns}.data
execute if score #pu_max_duration {ns}.data matches 1.. run scoreboard players operation #pu_seconds {ns}.data /= #20 {ns}.data
execute if score #pu_max_duration {ns}.data matches 1.. run bossbar set {ns}:{bossbar_id} name [{{"text":"{display_name} - ","color":"{color}","bold":true}},{{"score":{{"name":"#pu_seconds","objective":"{ns}.data"}},"color":"{color}"}},"s"]
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Hooks into existing systems
	# ──────────────────────────────────────────────────────────────────────────

	# Bossbar update calls for game_tick, generated from TIMED_POWERUPS
	bb_update_calls: str = "\n".join(
		f"function {ns}:v{version}/zombies/powerups/update_{pu_id}_bb"
		for pu_id in TIMED_POWERUPS
	)

	# Scoreboard decrement calls for game_tick, generated from TIMED_POWERUPS
	decrement_calls: str = "\n".join(
		f"execute as @a[scores={{{ns}.special.{v['scoreboard']}=1..}}] run scoreboard players remove @s {ns}.special.{v['scoreboard']} 1"
		for k, v in TIMED_POWERUPS.items()
		if k not in ("insta_kill", "unlimited_ammo") # They are already handled globally (not zombies)
	)

	write_versioned_function("zombies/game_tick", f"""
# Power-up entity tick (lifetime countdown, blink, pickup detection)
execute as @e[tag={ns}.pu_item] at @s run function {ns}:v{version}/zombies/powerups/entity_tick

# Blink state: toggles between 0 and 1 every 4 ticks (~0.2s half-cycle, matching BO2's 0.4s full cycle)
scoreboard players add #zb_blink_counter {ns}.data 1
execute if score #zb_blink_counter {ns}.data matches 4.. run scoreboard players set #zb_blink_counter {ns}.data 0
execute if score #zb_blink_counter {ns}.data matches 0 run scoreboard players add #zb_blink_state {ns}.data 1
execute if score #zb_blink_state {ns}.data matches 2.. run scoreboard players set #zb_blink_state {ns}.data 0

# Decrement duration scoreboards
{decrement_calls}

# Update bossbars
{bb_update_calls}
""")

	# stop cleanup resets, generated from TIMED_POWERUPS
	stop_scoreboard_resets: str = "\n".join(
		f"scoreboard players set @a {ns}.special.{v['scoreboard']} 0"
		for v in TIMED_POWERUPS.values()
	)
	stop_bossbar_removes: str = "\n".join(
		f"bossbar remove {ns}:{v['bossbar_id']}"
		for v in TIMED_POWERUPS.values()
	)

	write_versioned_function("zombies/stop", f"""
# Power-up cleanup
kill @e[tag={ns}.pu_item]
kill @e[tag={ns}.pu_text]
scoreboard players set #zb_drops_this_round {ns}.data 0
scoreboard players set #zb_score_to_drop {ns}.data 0
{stop_scoreboard_resets}
data modify storage {ns}:data _pu_queue set value []

# Remove all duration-based bossbars
{stop_bossbar_removes}
""")

	write_versioned_function("zombies/start_round", f"""
# Reset per-round power-up drop counter
scoreboard players set #zb_drops_this_round {ns}.data 0

# Threshold = sum of all in-game player points at round start + 2000
scoreboard players set #zb_score_to_drop {ns}.data 2000
scoreboard players operation #zb_score_to_drop {ns}.data += @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points
""")

	write_versioned_function("zombies/check_kill_points", f"""
# Double points bonus: award the same kill points again if active
execute if score @s {ns}.special.double_points matches 1.. run scoreboard players operation @s {ns}.zb.points += #total_kill_points {ns}.data
""")

	write_versioned_function("zombies/on_hit_signal", f"""
# Double points bonus for bullet hit points
execute if score @n[tag={ns}.ticking] {ns}.special.double_points matches 1.. run scoreboard players operation @n[tag={ns}.ticking] {ns}.zb.points += #zb_points_hit {ns}.config
""")

