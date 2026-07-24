
# ruff: noqa: E501
# Power-up System
# On each zombie death there is a min(5%, 2/total_round_zombies) chance to drop a power-up,
# until one full shuffle-bag cycle has dropped this round. Rares only appear after round 5.
# Visual: item entity + text_display. Pickup by proximity (1.5 blocks). 26.5s lifetime.
from stewbeet import JsonDict, LootTable, Mem, set_json_encoder, write_load_file, write_versioned_function

from ..helpers import MGS_TAG

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
# Optional sound keys (all relative to {ns}:zombies/powerups/):
#   sound       - activation sound
#   additional  - a second sound played simultaneously with `sound`
#   end_sound    - (timed power-ups) played once when the effect expires
POWERUP_TYPES: dict[str, JsonDict] = {
	"max_ammo":       {"item": "minecraft:amethyst_shard",       "display": "Max Ammo",       "color": "aqua",         "type_num": 1, "tier": "common", "sound": "max_ammo", "additional": "max_ammo_additional"},
	"insta_kill":     {"item": "minecraft:fermented_spider_eye", "display": "Insta Kill",     "color": "red",          "type_num": 2, "tier": "common", "duration": 600, "scoreboard": "instant_kill",  "bossbar_id": "pu_insta_kill",     "bb_color": "red",    "sound": "insta_kill", "end_sound": "insta_kill_off"},
	"double_points":  {"item": "minecraft:gold_ingot",           "display": "Double Points",  "color": "yellow",       "type_num": 3, "tier": "common", "duration": 600, "scoreboard": "double_points", "bossbar_id": "pu_double_points",  "bb_color": "yellow", "sound": "double_points", "end_sound": "double_points_off"},
	"carpenter":      {"item": "minecraft:oak_log",              "display": "Carpenter",      "color": "gold",         "type_num": 4, "tier": "common", "sound": "carpenter"},
	"nuke":           {"item": "minecraft:tnt",                  "display": "Nuke",           "color": "red",          "type_num": 5, "tier": "common", "sound": "nuke", "additional": "nuke_additional"},
	"unlimited_ammo": {"item": "minecraft:blaze_rod",            "display": "Unlimited Ammo", "color": "green",        "type_num": 6, "tier": "rare",   "duration": 600, "scoreboard": "infinite_ammo", "bossbar_id": "pu_unlimited_ammo", "bb_color": "green"},
	"random_perk":    {"item": "minecraft:glass_bottle",         "display": "Random Perk",    "color": "light_purple", "type_num": 7, "tier": "rare",   "sound": "random_perk"},
	"free_pap":       {"item": "minecraft:diamond",              "display": "Free PAP",       "color": "aqua",         "type_num": 8, "tier": "rare"},
	"cash_drop":      {"item": "minecraft:emerald",              "display": "Cash Drop",      "color": "green",        "type_num": 9, "tier": "rare",   "sound": "bonus_points"},
	"fire_sale":      {"item": "minecraft:firework_star",        "display": "Fire Sale",      "color": "light_purple", "type_num": 10, "tier": "rare",  "sound": "fire_sale"},
	"bonfire_sale":   {"item": "minecraft:campfire",             "display": "Bonfire Sale",   "color": "gold",         "type_num": 11, "tier": "rare",  "sound": "bonfire_sale"},
}

POWERUP_LIFETIME: int    = 530  # 26.5 seconds in ticks
POWERUP_BLINK_START: int = 200  # Blink warning when this many ticks remain (~10s)
FIRE_SALE_DURATION: int  = 600  # 30 seconds in ticks: Mystery Box costs 10 points
BONFIRE_SALE_DURATION: int = 600  # 30 seconds in ticks: Pack-a-Punch costs 200 points (1000/5)

# Convenience view: only power-ups with a timed duration
TIMED_POWERUPS: dict[str, JsonDict] = {k: v for k, v in POWERUP_TYPES.items() if "duration" in v}


def generate_powerups() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Helper: a power-up sound played for all in-game players (volume kept modest on purpose).
	def pu_snd(name: str, vol: float = 0.7, pitch: float = 1.0, at_s: bool = False) -> str:
		# Power-ups affect everyone, so their cues must be GLOBAL (non-positional): play the sound at
		# each in-game player's OWN position so all players hear it at full volume regardless of how far
		# they were from the power-up. `at_s` returns a bare fragment for use after `execute if ...`.
		body = f"as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/powerups/{name} ambient @s ~ ~ ~ {vol} {pitch}"
		return body if at_s else f"execute {body}"

	# Activation sound line(s) for a power-up entry, including its "additional" layer if present.
	def pu_activate_sound(v: JsonDict, vol: float = 1.0) -> str:
		if "sound" not in v:
			return f"playsound minecraft:entity.player.levelup ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0"
		lines = [pu_snd(v["sound"], vol)]
		if "additional" in v:
			lines.append(pu_snd(v["additional"], vol))
		return "\n".join(lines)

	# ──────────────────────────────────────────────────────────────────────────
	# Scoreboards
	# ──────────────────────────────────────────────────────────────────────────
	write_load_file(f"""
# Power-up entity scoreboards
scoreboard objectives add {ns}.zb.pu.type dummy
scoreboard objectives add {ns}.zb.pu.timer dummy
# Per-zombie: tick of the last time a player's weapon hit it (gates drops to player kills)
scoreboard objectives add {ns}.zb.player_hit dummy
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
# Only drop when a player's weapon killed this zombie (hit within the last 100 ticks),
# never from nukes/traps/environmental deaths. @s = the dying zombie.
scoreboard players operation #pu_hit_cutoff {ns}.data = #total_tick {ns}.data
scoreboard players remove #pu_hit_cutoff {ns}.data 100
execute unless score @s {ns}.zb.player_hit >= #pu_hit_cutoff {ns}.data run return 0

# Stop once a full drop cycle (one shuffle-bag worth) has dropped this round
execute if score #zb_cycle_done {ns}.data matches 1 run return 0

# Drop chance = min(2%, 2/total_round_zombies), expressed in basis points (per 10000).
# 2% = 200 bp; 1/total = 10000/total bp. Take the smaller of the two.
scoreboard players set #pu_chance_bp {ns}.data 200
execute if score #zb_round_total {ns}.data matches 1.. run scoreboard players set #pu_chance_tmp {ns}.data 10000
execute if score #zb_round_total {ns}.data matches 1.. run scoreboard players operation #pu_chance_tmp {ns}.data /= #zb_round_total {ns}.data
execute if score #zb_round_total {ns}.data matches 1.. if score #pu_chance_tmp {ns}.data < #pu_chance_bp {ns}.data run scoreboard players operation #pu_chance_bp {ns}.data = #pu_chance_tmp {ns}.data

# Roll against the chance
execute store result score #pu_rng_roll {ns}.data run random value 1..10000
execute unless score #pu_rng_roll {ns}.data <= #pu_chance_bp {ns}.data run return 0

# Passed: draw and spawn at this entity's position
function {ns}:v{version}/zombies/powerups/spawn_random_at_self

# Count the drop; once a full cycle has dropped, no more drops this round
scoreboard players add #zb_drops_this_round {ns}.data 1
execute if score #zb_drops_this_round {ns}.data >= #zb_cycle_len {ns}.data run scoreboard players set #zb_cycle_done {ns}.data 1
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
function {ns}:v{version}/zombies/powerups/do_spawn_random
""")

	# The shuffle bag deals a type_num; name it, then take the same route as an intercepted item
	do_spawn_random_lines: str = "\n".join(
		f'execute if score #pu_spawn_type {ns}.data matches {v["type_num"]} run data modify storage {ns}:temp _pu_spawn.type set value "{pu_id}"'
		for pu_id, v in POWERUP_TYPES.items()
	)
	write_versioned_function("zombies/powerups/do_spawn_random", f"""
{do_spawn_random_lines}
function {ns}:v{version}/zombies/powerups/spawn_display with storage {ns}:temp _pu_spawn
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
	# Rares are gated to after round 5 (round 6+), then each has an independent 25% chance.
	queue_refill_rare_lines: str = "\n".join(
		f"execute if score #zb_round {ns}.data matches 6.. store result score #pu_rare_roll_{v['type_num']} {ns}.data run random value 1..100\n"
		f"execute if score #zb_round {ns}.data matches 6.. if score #pu_rare_roll_{v['type_num']} {ns}.data matches 1..25 run data modify storage {ns}:data _pu_queue append value {v['type_num']}"
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

	# Dispatch to the shared spawner, carrying everything that differs per type as macro arguments.
	# The floating label stays a literal text component here (quoted so it survives as one argument)
	# so auto.lang_file still lifts the English out of it — hence `label:`, not `text:`, as the
	# argument name, or the outer quoted value would be the one that gets translated.
	dispatch_lines: str = "\n".join(
		f'$execute if data storage {ns}:temp _pu_spawn {{"type":"{pu_id}"}} run function {ns}:v{version}/zombies/powerups/spawn_type '
		f'{{x:$(x),y:$(y),z:$(z),uid:$(uid),item:"{v["item"]}",type_num:{v["type_num"]},'
		f'label:\'{{"text":"{v["display"]}","color":"{v["color"]}","bold":true}}\'}}'
		for pu_id, v in POWERUP_TYPES.items()
	)
	write_versioned_function("zombies/powerups/spawn_display", f"""
{dispatch_lines}
""")

	# Shared spawner (macro: x, y, z, uid, item, type_num, label)
	write_versioned_function("zombies/powerups/spawn_type", f"""
$summon minecraft:item $(x) $(y) $(z) {{Tags:["{ns}.pu_item","{ns}.pu_item_new","{ns}.gm_entity"],PickupDelay:32767,Invulnerable:1b,Item:{{id:"$(item)",count:1,components:{{"minecraft:custom_data":{{{ns}:{{powerup_uid:$(uid)}}}}}}}}}}
$scoreboard players set @n[type=minecraft:item,tag={ns}.pu_item_new] {ns}.zb.pu.type $(type_num)
scoreboard players set @n[type=minecraft:item,tag={ns}.pu_item_new] {ns}.zb.pu.timer {POWERUP_LIFETIME}
tag @n[type=minecraft:item,tag={ns}.pu_item_new] remove {ns}.pu_item_new

# Track live power-up count so game_tick can gate the per-item scans (decremented on expire/pickup,
# reset to 0 by the bulk cleanup, resynced periodically). pu_item is Invulnerable, so it can only die
# through those tracked paths — the count can never under-count and freeze a live power-up.
scoreboard players add #pu_active {ns}.data 1
$execute positioned $(x) $(y) $(z) run summon minecraft:text_display ~ ~1.0 ~ {{Tags:["{ns}.pu_text","{ns}.gm_entity"],text:$(label),billboard:"vertical",background:0,shadow:true,view_range:64.0f,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.5f,1.5f,1.5f]}}}}

# Drop spawn cue
{pu_snd("item/spawn", 0.7)}
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Entity tick: lifetime, blink, pickup detection
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/powerups/entity_tick", f"""
# Decrement lifetime timer
scoreboard players operation @s {ns}.zb.pu.timer -= #tick_delta {ns}.data

# Expired: remove visuals and stop processing this entity
execute if score @s {ns}.zb.pu.timer matches ..0 run return run function {ns}:v{version}/zombies/powerups/expire

# Blink warning in the last {POWERUP_BLINK_START // 20} seconds
execute if score @s {ns}.zb.pu.timer matches 1..{POWERUP_BLINK_START - 1} run function {ns}:v{version}/zombies/powerups/blink_tick

# Ambient loop: play loop_2s at the item every 2 seconds (40 ticks)
scoreboard players operation #pu_loop_phase {ns}.data = @s {ns}.zb.pu.timer
scoreboard players operation #pu_loop_phase {ns}.data %= #40 {ns}.data
execute if score #pu_loop_phase {ns}.data matches 0 run playsound {ns}:zombies/powerups/item/loop_2s ambient @a[scores={{{ns}.zb.in_game=1}},distance=..24] ~ ~ ~ 0.5 1.0

# Pickup check (do_pickup kills @s, so this must be the last command)
execute if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5,tag=!{ns}.pu_collecting] run function {ns}:v{version}/zombies/powerups/do_pickup

# Downed players pick up power-ups by crawling their mannequin over them (Black Ops rule).
# Only fires when no alive player is in range (alive players take priority and already ran above).
execute unless entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5] if entity @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,distance=..1.5] run function {ns}:v{version}/zombies/powerups/do_pickup
""")

	write_versioned_function("zombies/powerups/expire", f"""
kill @n[type=minecraft:text_display,tag={ns}.pu_text,distance=..3]
kill @s
scoreboard players remove #pu_active {ns}.data 1
""")

	# Blink implementation matching BO2's ~0.4s full cycle (4 ticks on, 4 ticks off).
	write_versioned_function("zombies/powerups/blink_tick", f"""
# "Off" frame: hide the item entity and the text_display
execute if score #zb_blink_state {ns}.data matches 0 run data modify entity @s Item.components."minecraft:custom_data".{ns}.powerup_model set from entity @s Item.components."minecraft:item_model"
execute if score #zb_blink_state {ns}.data matches 0 run data modify entity @s Item.components."minecraft:item_model" set value "minecraft:air"
# "On" frame: show the item entity again
execute if score #zb_blink_state {ns}.data matches 1 run data modify entity @s Item.components."minecraft:item_model" set from entity @s Item.components."minecraft:custom_data".{ns}.powerup_model
# text_display has no generic visibility tag — use view_range toggle instead
execute if score #zb_blink_state {ns}.data matches 0 as @n[type=minecraft:text_display,tag={ns}.pu_text,distance=..3] run data merge entity @s {{view_range:0.0f}}
execute if score #zb_blink_state {ns}.data matches 1 as @n[type=minecraft:text_display,tag={ns}.pu_text,distance=..3] run data merge entity @s {{view_range:64.0f}}
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Pickup
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/powerups/do_pickup", f"""
# Tag the nearest eligible player as the collector for this activation
tag @p[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5,tag=!{ns}.pu_collecting] add {ns}.pu_collecting

# If no alive player collected, a downed player crawled their mannequin over it: credit them.
execute unless entity @a[tag={ns}.pu_collecting] if entity @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,distance=..1.5] run function {ns}:v{version}/zombies/powerups/pickup_downed_collector

# Store power-up type before killing the entity
scoreboard players operation #pu_type_pickup {ns}.data = @s {ns}.zb.pu.type

# Kill the text display first (we still have a valid position)
kill @n[type=minecraft:text_display,tag={ns}.pu_text,distance=..3]

# Grab cue
{pu_snd("item/grab", 0.4)}

# Activate the power-up effect (collector tag is still active here)
function {ns}:v{version}/zombies/powerups/dispatch_activate

# Kill this power-up item entity
kill @s
scoreboard players remove #pu_active {ns}.data 1

# Clean up the collector tag so other pickups can proceed
tag @a[tag={ns}.pu_collecting] remove {ns}.pu_collecting
""")

	# Tag the owner of the nearest downed mannequin (a downed spectator) as the collector,
	# so a crawling downed player can grab power-ups. @s = the power-up item entity.
	write_versioned_function("zombies/powerups/pickup_downed_collector", f"""
scoreboard players set #pu_downed_id {ns}.data -1
execute as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,distance=..1.5,sort=nearest,limit=1] run scoreboard players operation #pu_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @a[tag={ns}.downed_spectator,scores={{{ns}.zb.in_game=1}}] if score @s {ns}.zb.downed_id = #pu_downed_id {ns}.data run tag @s add {ns}.pu_collecting
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

	## 1. Max Ammo (no chat message — the sound is enough)
	write_versioned_function("zombies/powerups/activate/max_ammo", f"""
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:zombies/bonus/max_ammo
{pu_activate_sound(POWERUP_TYPES["max_ammo"])}
""")

	## 2-4. Timed power-ups: Insta Kill, Double Points, Unlimited Ammo
	# All share the same bossbar+scoreboard activation pattern, driven by TIMED_POWERUPS.
	for pu_id, v in TIMED_POWERUPS.items():
		duration: int     = v["duration"]
		scoreboard: str   = v["scoreboard"]
		bossbar_id: str   = v["bossbar_id"]
		display_name: str = v["display"]
		bb_color: str     = v["bb_color"]
		write_versioned_function(f"zombies/powerups/activate/{pu_id}", f"""
scoreboard players set @a[scores={{{ns}.zb.in_game=1}}] {ns}.special.{scoreboard} {duration}
bossbar remove {ns}:{bossbar_id}
bossbar add {ns}:{bossbar_id} {{"text":"{display_name}","bold":true,"color":"{bb_color}"}}
bossbar set {ns}:{bossbar_id} max {duration}
bossbar set {ns}:{bossbar_id} value {duration}
bossbar set {ns}:{bossbar_id} color {bb_color}
bossbar set {ns}:{bossbar_id} style progress
bossbar set {ns}:{bossbar_id} players @a[scores={{{ns}.zb.in_game=1}}]
{pu_activate_sound(v)}
""")

	## 5. Carpenter (instant barrier repair) — no chat message; +200 points, doubled with Double Points
	write_versioned_function("zombies/powerups/activate/carpenter", f"""
function {ns}:v{version}/zombies/barriers/repair_all
{pu_snd("carpenter")}
scoreboard players add @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points 200
scoreboard players add @a[scores={{{ns}.zb.in_game=1,{ns}.special.double_points=1..}}] {ns}.zb.points 200
""")

	## 6. Nuke — kaboom + soul layer, white screen flash, zombies catch fire (no chat message).
	## +400 points to everyone, doubled to +800 for players with Double Points.
	write_versioned_function("zombies/powerups/activate/nuke", f"""
execute as @a[tag={ns}.pu_collecting,scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:zombies/bonus/nuke
scoreboard players add @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points 400
scoreboard players add @a[scores={{{ns}.zb.in_game=1,{ns}.special.double_points=1..}}] {ns}.zb.points 400

# Kaboom + additional layer + soul whoosh (played together)
{pu_snd("nuke")}
{pu_snd("nuke_additional")}
{pu_snd("nuke_soul", 0.8)}

# White screen flash for ~1s (blindness fades to white), and set every zombie on fire
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/powerups/nuke_flash
execute as @e[tag={ns}.nukable] at @s run function {ns}:v{version}/zombies/powerups/nuke_fire_one
""")

	## Nuke white-flash for a player: the firework 'flash' particle renders a brief white fullscreen
	## flash when emitted at the camera (Black Ops nuke screen flash).
	write_versioned_function("zombies/powerups/nuke_flash", """
execute at @s anchored eyes run particle minecraft:flash{color:[1.0,1.0,1.0,1.0]} ^ ^ ^0.4 0 0 0 0 1 force @s
""")

	## Set one zombie on fire + emit fire particles (called as @s = nukable entity)
	write_versioned_function("zombies/powerups/nuke_fire_one", f"""
data merge entity @s {{Fire:1200s}}
effect give @s minecraft:fire_resistance infinite 0 true
particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.02 12 force @a[scores={{{ns}.zb.in_game=1}},distance=..48]
particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.02 6 force @a[scores={{{ns}.zb.in_game=1}},distance=..48]
""")

	## 7. Random Perk — draws from the shared available-perk pool (perks placed on THIS map,
	## unowned by the collector). See zombies/perks.py `pool/*` (README task 4).
	write_versioned_function("zombies/powerups/activate/random_perk", f"""
# Pick a random unowned perk from the map's placed perks for the collecting player
tag @p[tag={ns}.pu_collecting] add {ns}.pool_target
scoreboard players set #pool_all_perks {ns}.data 0
function {ns}:v{version}/zombies/perks/pool/choose
tag @a[tag={ns}.pool_target] remove {ns}.pool_target

# Nothing available: the collector already owns every perk placed on this map
execute if score #pool_chosen {ns}.data matches ..-1 run return run tellraw @p[tag={ns}.pu_collecting] [{MGS_TAG},{{"text":"You already own every perk on the map!","color":"yellow"}}]

# Grant the chosen perk to the collector
execute as @p[tag={ns}.pu_collecting] run function {ns}:v{version}/zombies/perks/apply with storage {ns}:temp _pool

# Announce + sound
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Random Perk dropped for ","color":"light_purple"}},{{"selector":"@p[tag={ns}.pu_collecting]","color":"light_purple","bold":true}},{{"text":"!","color":"light_purple"}}]
{pu_snd("random_perk")}
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
{pu_snd("bonus_points")}
""")

	## 10. Fire Sale: Mystery Box costs 10 points for {FIRE_SALE_DURATION // 20}s (global timer + bossbar)
	write_versioned_function("zombies/powerups/activate/fire_sale", f"""
# Remember whether a Fire Sale was already running (so we don't re-trigger song/temp boxes)
scoreboard players set #fs_was_active {ns}.data 0
execute if score #zb_fire_sale_timer {ns}.data matches 1.. run scoreboard players set #fs_was_active {ns}.data 1

# Save the normal price only when no Fire Sale is already running (so we don't snapshot the discount)
execute if score #zb_fire_sale_timer {ns}.data matches ..0 run scoreboard players operation #zb_fire_sale_saved {ns}.data = #zb_mystery_box_price {ns}.config

# Apply the discount and (re)start the timer
scoreboard players set #zb_mystery_box_price {ns}.config 10
scoreboard players set #zb_fire_sale_timer {ns}.data {FIRE_SALE_DURATION}

# Bossbar
bossbar remove {ns}:pu_fire_sale
bossbar add {ns}:pu_fire_sale {{"text":"Fire Sale","bold":true,"color":"light_purple"}}
bossbar set {ns}:pu_fire_sale max {FIRE_SALE_DURATION}
bossbar set {ns}:pu_fire_sale value {FIRE_SALE_DURATION}
bossbar set {ns}:pu_fire_sale color pink
bossbar set {ns}:pu_fire_sale style progress
bossbar set {ns}:pu_fire_sale players @a[scores={{{ns}.zb.in_game=1}}]

# Only on a NEW Fire Sale: jingle + song (don't restack the song) + temp boxes everywhere
execute if score #fs_was_active {ns}.data matches 0 run {pu_snd("fire_sale")}
execute if score #fs_was_active {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}}] run playsound {ns}:zombies/powerups/fire_sale_song ambient @s ~ ~ ~ 0.3 1.0
execute if score #fs_was_active {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/fire_sale_start
""")

	## Fire Sale global tick: countdown, bossbar update, restore price on expiry
	write_versioned_function("zombies/powerups/fire_sale_tick", f"""
# Decrement the shared timer
scoreboard players operation #zb_fire_sale_timer {ns}.data -= #tick_delta {ns}.data

# Expired: restore the saved price, remove the bossbar, stop the song, remove temp boxes
execute if score #zb_fire_sale_timer {ns}.data matches ..0 run scoreboard players operation #zb_mystery_box_price {ns}.config = #zb_fire_sale_saved {ns}.data
execute if score #zb_fire_sale_timer {ns}.data matches ..0 run bossbar remove {ns}:pu_fire_sale
execute if score #zb_fire_sale_timer {ns}.data matches ..0 run stopsound @a[scores={{{ns}.zb.in_game=1}}] ambient {ns}:zombies/powerups/fire_sale_song
execute if score #zb_fire_sale_timer {ns}.data matches ..0 run function {ns}:v{version}/zombies/mystery_box/fire_sale_end

# Still active: update bossbar value
execute if score #zb_fire_sale_timer {ns}.data matches 1.. store result bossbar {ns}:pu_fire_sale value run scoreboard players get #zb_fire_sale_timer {ns}.data
""")

	## 11. Bonfire Sale: Pack-a-Punch costs 200 (1000/5) for {BONFIRE_SALE_DURATION // 20}s
	write_versioned_function("zombies/powerups/activate/bonfire_sale", f"""
scoreboard players set #zb_bonfire_sale_timer {ns}.data {BONFIRE_SALE_DURATION}

# Bossbar
bossbar remove {ns}:pu_bonfire_sale
bossbar add {ns}:pu_bonfire_sale {{"text":"Bonfire Sale","bold":true,"color":"gold"}}
bossbar set {ns}:pu_bonfire_sale max {BONFIRE_SALE_DURATION}
bossbar set {ns}:pu_bonfire_sale value {BONFIRE_SALE_DURATION}
bossbar set {ns}:pu_bonfire_sale color yellow
bossbar set {ns}:pu_bonfire_sale style progress
bossbar set {ns}:pu_bonfire_sale players @a[scores={{{ns}.zb.in_game=1}}]
{pu_snd("bonfire_sale")}
""")

	## Bonfire Sale global tick: countdown + bossbar, clears itself on expiry
	write_versioned_function("zombies/powerups/bonfire_sale_tick", f"""
scoreboard players operation #zb_bonfire_sale_timer {ns}.data -= #tick_delta {ns}.data
execute if score #zb_bonfire_sale_timer {ns}.data matches ..0 run bossbar remove {ns}:pu_bonfire_sale
execute if score #zb_bonfire_sale_timer {ns}.data matches 1.. store result bossbar {ns}:pu_bonfire_sale value run scoreboard players get #zb_bonfire_sale_timer {ns}.data
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Bossbar update functions — generated from TIMED_POWERUPS, one per entry
	# ──────────────────────────────────────────────────────────────────────────
	for pu_id, v in TIMED_POWERUPS.items():
		scoreboard: str   = v["scoreboard"]
		bossbar_id: str   = v["bossbar_id"]
		display_name: str = v["display"]
		# Play the end sound once when the effect transitions from active to expired
		end_sound_line: str = ""
		if "end_sound" in v:
			end_sound: str = pu_snd(v["end_sound"], at_s=True)
			end_sound_line = f"execute if score #pu_prev_{pu_id} {ns}.data matches 1.. if score #pu_max_duration {ns}.data matches ..0 {end_sound}\n"
		write_versioned_function(f"zombies/powerups/update_{pu_id}_bb", f"""
# Find max remaining duration across all players with active {pu_id}
scoreboard players set #pu_max_duration {ns}.data 0
scoreboard players operation #pu_max_duration {ns}.data > @a[scores={{{ns}.special.{scoreboard}=1..}}] {ns}.special.{scoreboard}

# Steady-off fast path: inactive now AND last tick -> no bossbar command at all
# (the bossbar remove used to run every single tick while the powerup was inactive)
execute if score #pu_max_duration {ns}.data matches ..0 if score #pu_prev_{pu_id} {ns}.data matches ..0 run return 0

# If max duration just hit 0, remove bossbar (once); otherwise update value
execute if score #pu_max_duration {ns}.data matches ..0 run bossbar remove {ns}:{bossbar_id}
execute if score #pu_max_duration {ns}.data matches 1.. store result bossbar {ns}:{bossbar_id} value run scoreboard players get #pu_max_duration {ns}.data
{end_sound_line}scoreboard players operation #pu_prev_{pu_id} {ns}.data = #pu_max_duration {ns}.data
""")

	# ──────────────────────────────────────────────────────────────────────────
	# Hooks into existing systems
	# ──────────────────────────────────────────────────────────────────────────

	## Insta-kill melee modifier transitions (tag-gated from game_tick above)
	write_versioned_function("zombies/powerups/insta_kill_melee_on", f"""
# remove-then-add keeps this idempotent even if a stale modifier survived a game crash
attribute @s minecraft:attack_damage modifier remove {ns}:insta_kill
attribute @s minecraft:attack_damage modifier add {ns}:insta_kill 100000 add_value
tag @s add {ns}.ik_melee
""")
	write_versioned_function("zombies/powerups/insta_kill_melee_off", f"""
attribute @s minecraft:attack_damage modifier remove {ns}:insta_kill
tag @s remove {ns}.ik_melee
""")

	# Bossbar update calls for game_tick, generated from TIMED_POWERUPS
	bb_update_calls: str = "\n".join(
		f"function {ns}:v{version}/zombies/powerups/update_{pu_id}_bb"
		for pu_id in TIMED_POWERUPS
	)

	# Scoreboard decrement calls for game_tick, generated from TIMED_POWERUPS
	decrement_calls: str = "\n".join(
		f"execute as @a[scores={{{ns}.special.{v['scoreboard']}=1..}}] run scoreboard players operation @s {ns}.special.{v['scoreboard']} -= #tick_delta {ns}.data"
		for k, v in TIMED_POWERUPS.items()
		if k not in ("insta_kill", "unlimited_ammo") # They are already handled globally (not zombies)
	)

	write_versioned_function("zombies/game_tick", f"""
# Power-up entities exist only after a drop. #pu_active (maintained on spawn/expire/pickup) gates the
# two per-tick scans below so an empty board costs nothing. Resync once every 40 ticks as a safety net
# (the count is already exact since pu_item is Invulnerable and only dies through tracked paths).
execute store result score #pu_active_phase {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #pu_active_phase {ns}.data %= #40 {ns}.data
execute if score #pu_active_phase {ns}.data matches 0 store result score #pu_active {ns}.data if entity @e[type=minecraft:item,tag={ns}.pu_item]

# Power-up entity tick (lifetime countdown, blink, pickup detection)
execute if score #pu_active {ns}.data matches 1.. as @e[type=minecraft:item,tag={ns}.pu_item] at @s run function {ns}:v{version}/zombies/powerups/entity_tick

# Orphan cleanup: a text_display whose item entity was destroyed (burned/exploded) would never
# be removed by expire/pickup — kill any pu_text that no longer has a pu_item beneath it.
execute if score #pu_active {ns}.data matches 1.. as @e[type=minecraft:text_display,tag={ns}.pu_text] at @s unless entity @e[type=minecraft:item,tag={ns}.pu_item,distance=..4] run kill @s

# Insta Kill also works with the knife: give active players a huge melee attack damage so a single
# melee hit one-shots zombies (guns already insta-kill via the raycast path). The {ns}.ik_melee tag
# tracks who currently carries the modifier, so the attribute commands only run on state
# transitions (they used to run for EVERY player EVERY tick, mostly as guaranteed failures).
execute as @a[tag=!{ns}.ik_melee,scores={{{ns}.special.instant_kill=1..}}] run function {ns}:v{version}/zombies/powerups/insta_kill_melee_on
execute as @a[tag={ns}.ik_melee,scores={{{ns}.special.instant_kill=..0}}] run function {ns}:v{version}/zombies/powerups/insta_kill_melee_off

# Blink state: toggles between 0 and 1 every 4 ticks (~0.2s half-cycle, matching BO2's 0.4s full cycle)
scoreboard players add #zb_blink_counter {ns}.data 1
execute if score #zb_blink_counter {ns}.data matches 4.. run scoreboard players set #zb_blink_counter {ns}.data 0
execute if score #zb_blink_counter {ns}.data matches 0 run scoreboard players add #zb_blink_state {ns}.data 1
execute if score #zb_blink_state {ns}.data matches 2.. run scoreboard players set #zb_blink_state {ns}.data 0

# Decrement duration scoreboards
{decrement_calls}

# Update bossbars
{bb_update_calls}

# Fire Sale: global timer countdown + price restore on expiry
execute if score #zb_fire_sale_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/powerups/fire_sale_tick

# Bonfire Sale: global timer countdown
execute if score #zb_bonfire_sale_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/powerups/bonfire_sale_tick
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
kill @e[type=minecraft:item,tag={ns}.pu_item]
kill @e[type=minecraft:text_display,tag={ns}.pu_text]
scoreboard players set #pu_active {ns}.data 0
scoreboard players set #zb_drops_this_round {ns}.data 0
scoreboard players set #zb_cycle_done {ns}.data 0
scoreboard players set #zb_cycle_len {ns}.data 0
{stop_scoreboard_resets}
data modify storage {ns}:data _pu_queue set value []

# Fire Sale cleanup (reset the global timer + remove its bossbar + stop the song)
scoreboard players set #zb_fire_sale_timer {ns}.data 0
scoreboard players set #mb_fs_cleanup_pending {ns}.data 0
bossbar remove {ns}:pu_fire_sale
stopsound @a ambient {ns}:zombies/powerups/fire_sale_song
tag @e remove {ns}.mb_fs_active
tag @e remove {ns}.mb_orig_active
kill @e[tag={ns}.mb_temp]

# Bonfire Sale cleanup (reset the global timer + remove its bossbar)
scoreboard players set #zb_bonfire_sale_timer {ns}.data 0
bossbar remove {ns}:pu_bonfire_sale

# Remove all duration-based bossbars
{stop_bossbar_removes}
""")

	write_versioned_function("zombies/start_round", f"""
# Reset per-round power-up drop tracking
scoreboard players set #zb_drops_this_round {ns}.data 0
scoreboard players set #zb_cycle_done {ns}.data 0

# Start a fresh shuffle bag for the round; its size = one full drop cycle's worth of drops
function {ns}:v{version}/zombies/powerups/queue_refill
execute store result score #zb_cycle_len {ns}.data run data get storage {ns}:data _pu_queue
""")

	write_versioned_function("zombies/check_kill_points", f"""
# Double points bonus: award the same kill points again if active
execute if score @s {ns}.special.double_points matches 1.. run scoreboard players operation @s {ns}.zb.points += #total_kill_points {ns}.data
""")

	write_versioned_function("zombies/on_hit_signal", f"""
# Double points bonus for bullet hit points
execute if score @n[tag={ns}.ticking] {ns}.special.double_points matches 1.. run scoreboard players operation @n[tag={ns}.ticking] {ns}.zb.points += #zb_points_hit {ns}.config
""")
