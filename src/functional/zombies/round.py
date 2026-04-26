
# ruff: noqa: E501
# Zombies Round System
# Wave-based round progression with zombie spawning, scaling, and round completion.
from stewbeet import Mem, write_versioned_function


def generate_zombies_rounds() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Round System ──────────────────────────────────────────────

	## Start a new round
	write_versioned_function("zombies/start_round", f"""
# Increment round number
execute store result score #zb_round {ns}.data run data get storage {ns}:zombies game.round
scoreboard players add #zb_round {ns}.data 1
execute store result storage {ns}:zombies game.round int 1 run scoreboard players get #zb_round {ns}.data

# Calculate zombies to spawn this round: base formula = round * 4 + (player_count - 1) * 2
execute store result score #zb_player_count {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
scoreboard players remove #zb_player_count {ns}.data 1
scoreboard players operation #zb_player_count {ns}.data *= #2 {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data *= #4 {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data += #zb_player_count {ns}.data

# Store zombies to spawn and remaining count
scoreboard players operation #zb_remaining {ns}.data = #zb_to_spawn {ns}.data

# Calculate initial spawn timer and batch size for this round
function {ns}:v{version}/zombies/calc_spawn_timer

# Grace period: don't check game over for 3 seconds (60 ticks)
scoreboard players set #zb_round_grace {ns}.data 60

# Reset stuck zombie glow timers
scoreboard players set #zb_stuck_timer {ns}.data 0
scoreboard players set #zb_glow_timer {ns}.data 0

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 40 10
title @a[scores={{{ns}.zb.in_game=1}}] title [{{"text":"Round ","color":"red","bold":true}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}}]

# Signal round start
function #{ns}:zombies/on_round_start

# Refresh sidebar
function {ns}:v{version}/zombies/refresh_sidebar

# Announce
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"red"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" has begun!","color":"red"}}]
""")

	## Calculate spawn timer and batch size based on current round
	# Timer formula: max(1, 20 - round) → R1=38t, R10=20t, R20=1t+
	# Batch formula: floor((round - 1) / 50) + 1 → R1-50=1, R51-100=2, R101-150=3 ...
	write_versioned_function("zombies/calc_spawn_timer", f"""
# Timer: start at 20, clamp to minimum 1
scoreboard players set #zb_spawn_timer {ns}.data 20
scoreboard players operation #zb_spawn_timer {ns}.data -= #zb_round {ns}.data
execute if score #zb_spawn_timer {ns}.data matches ..1 run scoreboard players set #zb_spawn_timer {ns}.data 1

# Batch: (round - 1) / 50 + 1
scoreboard players operation #zb_spawn_batch {ns}.data = #zb_round {ns}.data
scoreboard players remove #zb_spawn_batch {ns}.data 1
scoreboard players operation #zb_spawn_batch {ns}.data /= #50 {ns}.data
scoreboard players add #zb_spawn_batch {ns}.data 1
""")

	## Spawn a single zombie using proximity-based selection from spawn markers
	write_versioned_function("zombies/spawn_zombie", f"""
# Tag nearby unlocked zombie spawns
# First pass: 32 blocks from any alive player
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked,distance=..32] add {ns}.zb_near

# Second pass: 64 blocks if none found
execute unless entity @e[tag={ns}.zb_near] as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked,distance=..64] add {ns}.zb_near

# Fallback: any unlocked spawn
execute unless entity @e[tag={ns}.zb_near] run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked] add {ns}.zb_near

# Pick random from tagged set and spawn
execute as @n[tag={ns}.zb_near,sort=random] at @s run function {ns}:v{version}/zombies/do_spawn_zombie

# Cleanup
tag @e[tag={ns}.zb_near] remove {ns}.zb_near
""")

	## Actually spawn the zombie at the marker position (@s = spawn marker, at @s)
	write_versioned_function("zombies/do_spawn_zombie", f"""
# Determine zombie level based on round
# Rounds 1-5: level 1, 6-10: level 2, 11-15: level 3, 16+: level 4
execute if score #zb_round {ns}.data matches ..5 run data modify storage {ns}:temp _zpos.level set value "1"
execute if score #zb_round {ns}.data matches 6..10 run data modify storage {ns}:temp _zpos.level set value "2"
execute if score #zb_round {ns}.data matches 11..15 run data modify storage {ns}:temp _zpos.level set value "3"
execute if score #zb_round {ns}.data matches 16.. run data modify storage {ns}:temp _zpos.level set value "4"

# Zombie type (normal for now; future: "armed", "fast", "tank")
data modify storage {ns}:temp _zpos.type set value "normal"

# Spawn the zombie (~ ~ ~ is spawn marker position, inherited from at @s in spawn_zombie)
function {ns}:v{version}/zombies/summon_zombie_at with storage {ns}:temp _zpos
""")

	## Summon zombie at execution position (macro for level/type dispatch)
	# Uses ~ ~-2 ~ so zombie spawns 2 blocks underground for the rise animation.
	# Execution context comes from: spawn_zombie → at @s (spawn marker) → do_spawn_zombie → here.
	write_versioned_function("zombies/summon_zombie_at", f"""
# Summon zombie 2 blocks underground with NoAI (rise animation in progress)
summon minecraft:zombie ~ ~-2 ~ {{Tags:["{ns}.zombie_round","{ns}.gm_entity","{ns}.nukable","{ns}.zb_rising"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty",NoAI:1b}}

# Apply type-specific scaling (health, speed, rise timer)
$execute as @n[tag={ns}.zombie_round,tag=!{ns}.zb_scaled] run function {ns}:v{version}/zombies/types/$(type) {{level:"$(level)"}}
""")

	# Enemy Types ───────────────────────────────────────────────
	# Each type function receives {level:"1"|"2"|"3"|"4"} as macro argument.
	# All types call the shared scale logic; stubs fall through to normal scaling.

	## Normal zombie: scale health/speed by level + start rise animation
	write_versioned_function("zombies/types/normal", f"""
tag @s add {ns}.zb_scaled

$scoreboard players set #zb_level {ns}.data $(level)

# Level 1: default 20 HP (rounds 1-5) — no changes needed
# Level 2: 30 HP (rounds 6-10)
execute if score #zb_level {ns}.data matches 2 run attribute @s minecraft:max_health base set 30
execute if score #zb_level {ns}.data matches 2 run data modify entity @s Health set value 30f

# Level 3: 40 HP (rounds 11-15)
execute if score #zb_level {ns}.data matches 3 run attribute @s minecraft:max_health base set 40
execute if score #zb_level {ns}.data matches 3 run data modify entity @s Health set value 40f

# Level 4: 60 HP (rounds 16+)
execute if score #zb_level {ns}.data matches 4 run attribute @s minecraft:max_health base set 60
execute if score #zb_level {ns}.data matches 4 run data modify entity @s Health set value 60f

# Increase speed slightly at higher levels
execute if score #zb_level {ns}.data matches 3 run attribute @s minecraft:movement_speed base set 0.26
execute if score #zb_level {ns}.data matches 4 run attribute @s minecraft:movement_speed base set 0.30

# Start rise animation (20 ticks to rise 2 blocks)
scoreboard players set @s {ns}.zb.rise_tick 20
""")

	## Armed zombie stub (TODO: carries weapon, drops ammo on death)
	write_versioned_function("zombies/types/armed", f"""
# TODO: armed zombie — unique AI goal: ranged attack, drops ammo powerup on death
# Falls through to normal scaling until implemented
$function {ns}:v{version}/zombies/types/normal {{level:"$(level)"}}
""")

	## Fast zombie stub (TODO: higher movement speed, less health)
	write_versioned_function("zombies/types/fast", f"""
# TODO: fast zombie — higher base movement speed, reduced health pool
# Falls through to normal scaling until implemented
$function {ns}:v{version}/zombies/types/normal {{level:"$(level)"}}
""")

	## Tank zombie stub (TODO: very high health, slow movement)
	write_versioned_function("zombies/types/tank", f"""
# TODO: tank zombie — very high health, reduced movement speed
# Falls through to normal scaling until implemented
$function {ns}:v{version}/zombies/types/normal {{level:"$(level)"}}
""")

	# Rise Animation ─────────────────────────────────────────────

	## Per-tick rise: called from game_tick for all zb_rising entities
	write_versioned_function("zombies/zombie_rise_tick", f"""
# Rise 0.1 blocks per tick
tp @s ~ ~0.1 ~

# Emit block-breaking particles from the block at the surface (2 blocks above spawn = ~0 now that we're rising)
# Read the block type at +2 above original spawn (approximately ground level)
execute positioned ~ ~ ~ run function #bs.block:get_type
data modify storage {ns}:temp _rise_particle.block set from storage bs:out block.type
function {ns}:v{version}/zombies/zombie_rise_particles with storage {ns}:temp _rise_particle

# Count down rise timer
scoreboard players remove @s {ns}.zb.rise_tick 1
execute if score @s {ns}.zb.rise_tick matches ..0 run function {ns}:v{version}/zombies/zombie_finish_rise
""")

	## Macro: emit block-textured particles at current position
	write_versioned_function("zombies/zombie_rise_particles", r"""
$execute align xyz run particle block{block_state:"$(block)"} ~.5 ~1 ~.5 0.3 0.1 0.3 0.5 15 force @a[distance=..64]
""")

	## Finish rise: activate AI and remove rising state
	write_versioned_function("zombies/zombie_finish_rise", f"""
data modify entity @s NoAI set value 0b
tag @s remove {ns}.zb_rising
""")

	## Spawn tick: spawn zombies on a timer
	write_versioned_function("zombies/spawn_tick", f"""
# Decrease spawn timer
scoreboard players remove #zb_spawn_timer {ns}.data 1
execute if score #zb_spawn_timer {ns}.data matches 1.. run return 0

# Timer fired: recalculate timer and batch size for next cycle
function {ns}:v{version}/zombies/calc_spawn_timer

# Spawn a batch of zombies (batch size depends on round)
scoreboard players operation #zb_spawn_batch_remaining {ns}.data = #zb_spawn_batch {ns}.data
function {ns}:v{version}/zombies/spawn_batch_tick
""")

	## Spawn batch tick: spawn up to #zb_spawn_batch zombies, one per call (recursive)
	write_versioned_function("zombies/spawn_batch_tick", f"""
# Guard: nothing left to spawn
execute if score #zb_to_spawn {ns}.data matches ..0 run return 0

# Spawn one zombie
function {ns}:v{version}/zombies/spawn_zombie
scoreboard players remove #zb_to_spawn {ns}.data 1
scoreboard players remove #zb_spawn_batch_remaining {ns}.data 1

# Recurse if batch not exhausted and zombies remain
execute if score #zb_spawn_batch_remaining {ns}.data matches 1.. if score #zb_to_spawn {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_batch_tick
""")

	# Round Completion ──────────────────────────────────────────

	write_versioned_function("zombies/round_complete", f"""
# Guard: prevent re-triggering every tick
scoreboard players set #zb_to_spawn {ns}.data -1

# Signal round end
function #{ns}:zombies/on_round_end

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 40 10
title @a[scores={{{ns}.zb.in_game=1}}] title [{{"text":"Round Complete!","color":"green","bold":true}}]

# Give all players 500 bonus points for surviving the round
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run scoreboard players add @s {ns}.zb.points 500

# Announce
execute store result score #completed_round {ns}.data run data get storage {ns}:zombies game.round
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"green"}},{{"score":{{"name":"#completed_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" complete! +500 points. Next round in 10 seconds...","color":"green"}}]

# Schedule next round after 10 seconds
schedule function {ns}:v{version}/zombies/start_round 200t

# Respawn all bled-out (spectator) players for the next round
function {ns}:v{version}/zombies/revive/round_respawn
""")

	# Grenade Replenishment (appended to start_round) ───────────

	write_versioned_function("zombies/start_round", f"""
# Replenish grenades for all alive players (+2, cap at 4)
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:v{version}/zombies/inventory/replenish_grenades
""")

	# Stuck Zombie Glow ──────────────────────────────────────────

	## Apply glowing to zombies far from all players (stuck/unreachable).
	## Called every 5s (100 ticks) once 60s have passed since the last zombie spawned.
	## Applies glowing for 6s (120 ticks) and clears it on zombies that moved near a player.
	write_versioned_function("zombies/glow_stuck_zombies", f"""
# Tag zombies currently within 32 blocks of any alive player
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run tag @e[tag={ns}.zombie_round,distance=..32] add {ns}.zb_near_player

# Apply glowing for 6 seconds to zombies far from all players
effect give @e[tag={ns}.zombie_round,tag=!{ns}.zb_near_player] glowing 6 0 true

# Cleanup temp tag
tag @e[tag={ns}.zb_near_player] remove {ns}.zb_near_player
""")

