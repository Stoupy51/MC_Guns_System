
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

# Calculate zombies to spawn this round: min(48, 7 + round) * min(4, player_count)
# Solo player: r1=8,  r5=12, r10=17, r20=27,  r40=47,  r41+ caps at 48
# 4+ players:  r1=32, r5=48, r10=68, r20=108, r40=188, r41+ caps at 192
execute store result score #zb_player_count {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
execute if score #zb_player_count {ns}.data matches 5.. run scoreboard players set #zb_player_count {ns}.data 4
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players add #zb_to_spawn {ns}.data 7
execute if score #zb_to_spawn {ns}.data matches 49.. run scoreboard players set #zb_to_spawn {ns}.data 48
scoreboard players operation #zb_to_spawn {ns}.data *= #zb_player_count {ns}.data

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
# Attach a marker passenger so death can be intercepted before vanilla event 60 (poof particles).
summon minecraft:zombie ~ ~-2 ~ {{Tags:["{ns}.zombie_round","{ns}.gm_entity","{ns}.nukable","{ns}.zb_rising"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty",NoAI:1b,Passengers:[{{id:"minecraft:marker",Tags:["{ns}.death_watch","{ns}.gm_entity"]}}]}}

# Apply type-specific scaling (health, speed, rise timer)
$execute as @n[tag={ns}.zombie_round,tag=!{ns}.zb_scaled] run function {ns}:v{version}/zombies/types/$(type) {{level:"$(level)"}}
""")

	# Enemy Types ───────────────────────────────────────────────
	# Each type function receives {level:"1"|"2"|"3"|"4"} as macro argument.
	# All types call the shared scale logic; stubs fall through to normal scaling.

	## Normal zombie: scale health/speed by level + start rise animation
	write_versioned_function("zombies/types/normal", f"""
# Add scaled tag
tag @s add {ns}.zb_scaled

# Delay visual death by 20 ticks
data modify entity @s DeathTime set value -20s

# Compute BO2-derived HP for this round and apply it to this zombie
function {ns}:v{version}/zombies/calc_zombie_hp
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp {ns}.data
function {ns}:v{version}/zombies/apply_zombie_hp with storage {ns}:temp _zb_hp

# Speed tiers from BO2 behavior (multiplier 8): walk R1-5, run R6-8, sprint R9+
execute if score #zb_round {ns}.data matches ..5 run attribute @s minecraft:movement_speed base set 0.18
execute if score #zb_round {ns}.data matches 6..8 run attribute @s minecraft:movement_speed base set 0.23
execute if score #zb_round {ns}.data matches 9 run attribute @s minecraft:movement_speed base set 0.30

# BO2-style walkers: R10+ has 10% chance to spawn as walk speed instead of sprint
execute if score #zb_round {ns}.data matches 10.. store result score #zb_speed_roll {ns}.data run random value 1..10
execute if score #zb_round {ns}.data matches 10.. if score #zb_speed_roll {ns}.data matches 1 run attribute @s minecraft:movement_speed base set 0.23
execute if score #zb_round {ns}.data matches 10.. if score #zb_speed_roll {ns}.data matches 2.. run attribute @s minecraft:movement_speed base set 0.30

# Start rise animation (20 ticks to rise 2 blocks)
scoreboard players set @s {ns}.zb.rise_tick 20
""")

	## Compute zombie HP for current round (BO2 formula adapted to Minecraft scale)
	write_versioned_function("zombies/calc_zombie_hp", f"""
# R1-9: linear growth
execute if score #zb_round {ns}.data matches ..9 run function {ns}:v{version}/zombies/calc_zombie_hp_linear

# R10+: exponential growth
execute if score #zb_round {ns}.data matches 10.. run function {ns}:v{version}/zombies/calc_zombie_hp_exp

# Cap at Minecraft-safe gameplay max
execute unless score #zb_hp {ns}.data matches 15..2048 run scoreboard players set #zb_hp {ns}.data 2048
""")

	## R1-9: (150 + (round - 1) * 100) * 2 / 15
	write_versioned_function("zombies/calc_zombie_hp_linear", f"""
scoreboard players operation #zb_hp {ns}.data = #zb_round {ns}.data
scoreboard players remove #zb_hp {ns}.data 1
scoreboard players operation #zb_hp {ns}.data *= #100 {ns}.data
scoreboard players operation #zb_hp {ns}.data += #150 {ns}.data
scoreboard players operation #zb_hp {ns}.data *= #2 {ns}.data
scoreboard players operation #zb_hp {ns}.data /= #15 {ns}.data
""")

	## R10+: 950 * 1.1^(round - 9) * 2 / 15
	write_versioned_function("zombies/calc_zombie_hp_exp", f"""
scoreboard players operation #zb_exp_round {ns}.data = #zb_round {ns}.data
scoreboard players remove #zb_exp_round {ns}.data 9

data modify storage bs:in math.pow.x set value 1.1f
execute store result storage bs:in math.pow.y float 1 run scoreboard players get #zb_exp_round {ns}.data
function #bs.math:pow

execute store result score #zb_hp {ns}.data run data get storage bs:out math.pow 950
scoreboard players operation #zb_hp {ns}.data *= #2 {ns}.data
scoreboard players operation #zb_hp {ns}.data /= #15 {ns}.data
""")

	## Apply computed HP to the current zombie (@s)
	write_versioned_function("zombies/apply_zombie_hp", """
$attribute @s minecraft:max_health base set $(val)
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get
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

	## Per-tick death watch: intercept zombie death before vanilla event 60 (poof particles)
	write_versioned_function("zombies/death_watch_tick", f"""
# Move execution from marker passenger -> vehicle (zombie), then intercept once DeathTime starts.
execute as @e[type=minecraft:marker,tag={ns}.death_watch] at @s on vehicle if data entity @s {{DeathTime:1s}} run function {ns}:v{version}/zombies/on_zombie_dying
""")

	## Intercept a dying zombie before DeathTime reaches 20
	write_versioned_function("zombies/on_zombie_dying", f"""
# Guard: only process round zombies.
execute unless entity @s[tag={ns}.zombie_round] run return 0

# Kill the attached death-watch marker while still mounted to avoid orphan buildup.
kill @n[type=minecraft:marker,tag={ns}.death_watch,distance=..1]

# Remove zombie before vanilla death event 60 can fire.
tp @s ~ -10000 ~
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

# Announce
execute store result score #completed_round {ns}.data run data get storage {ns}:zombies game.round
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"green"}},{{"score":{{"name":"#completed_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" complete! Next round in 5 seconds...","color":"green"}}]

# Schedule next round after 5 seconds
schedule function {ns}:v{version}/zombies/start_round 5s

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

	## Hook death watch into the main zombies game tick
	write_versioned_function("zombies/game_tick", f"""
# Intercept dying zombies before vanilla death particles are emitted.
function {ns}:v{version}/zombies/death_watch_tick
""")

	## Cleanup for round/end bulk-kill paths
	write_versioned_function("zombies/stop", f"""
kill @e[type=minecraft:marker,tag={ns}.death_watch]
""")

