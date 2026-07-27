""" The per-kill drop roll, the loot table behind it and the shuffle bag that picks a type. """
# Imports
from stewbeet import LootTable, Mem, set_json_encoder, write_load_file, write_versioned_function

from .types import POWERUP_TYPES


# Functions
def write_powerup_drops() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Scoreboards
	write_load_file(f"""
# Power-up entity scoreboards
scoreboard objectives add {ns}.zb.pu.type dummy
scoreboard objectives add {ns}.zb.pu.timer dummy
# Per-zombie: tick of the last time a player's weapon hit it (gates drops to player kills)
scoreboard objectives add {ns}.zb.player_hit dummy
""")

	# Loot table: equal-weight pool, each entry tags the item type
	Mem.ctx.data[ns].loot_tables["zombies/powerup_drop"] = set_json_encoder(LootTable({
		"pools": [{
			"rolls": 1,
			"entries": [
				{
					"type": "minecraft:item",
					"name": v.item,
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

	# Drop check — called from on_zombie_dying after position is stored
	write_versioned_function("zombies/powerups/check_drop", f"""
# Only drop when a player's weapon killed this zombie (hit within the last 100 ticks),
# never from nukes/traps/environmental deaths. @s = the dying zombie.
scoreboard players operation #pu_hit_cutoff {ns}.data = #total_tick {ns}.data
scoreboard players remove #pu_hit_cutoff {ns}.data 100
execute unless score @s {ns}.zb.player_hit >= #pu_hit_cutoff {ns}.data run return 0

# Stop once a full drop cycle (one shuffle-bag worth) has dropped this round
execute if score #zb_cycle_done {ns}.data matches 1 run return 0

# Drop chance = min(2%, 1/total_round_zombies), expressed in basis points (per 10000).
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
		f'execute if score #pu_spawn_type {ns}.data matches {v.type_num} run data modify storage {ns}:temp _pu_spawn.type set value "{pu_id}"'
		for pu_id, v in POWERUP_TYPES.items()
	)
	write_versioned_function("zombies/powerups/do_spawn_random", f"""
{do_spawn_random_lines}
function {ns}:v{version}/zombies/powerups/spawn_display with storage {ns}:temp _pu_spawn
""")

	# Shuffle-bag queue
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
		f"data modify storage {ns}:data _pu_queue append value {v.type_num}"
		for v in POWERUP_TYPES.values()
		if v.tier == "common"
	)
	# Rares are gated to after round 5 (round 6+), then each has an independent 25% chance.
	queue_refill_rare_lines: str = "\n".join(
		f"execute if score #zb_round {ns}.data matches 6.. store result score #pu_rare_roll_{v.type_num} {ns}.data run random value 1..100\n"
		f"execute if score #zb_round {ns}.data matches 6.. if score #pu_rare_roll_{v.type_num} {ns}.data matches 1..25 run data modify storage {ns}:data _pu_queue append value {v.type_num}"
		for v in POWERUP_TYPES.values()
		if v.tier == "rare"
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

