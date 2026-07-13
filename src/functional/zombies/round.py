
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

# Calculate zombies to spawn this round: min(256, min(96, 7 + round) * min(4, player_count))
# Solo player: r1=8,  r5=12, r10=17, r20=27,  r40=47,  r41+ caps at 96
# 4+ players:  r1=32, r5=48, r10=68, r20=108, r40=188, r41+ caps at 256
execute store result score #zb_player_count {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
execute if score #zb_player_count {ns}.data matches 5.. run scoreboard players set #zb_player_count {ns}.data 4
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players add #zb_to_spawn {ns}.data 7
execute if score #zb_to_spawn {ns}.data matches 97.. run scoreboard players set #zb_to_spawn {ns}.data 96
scoreboard players operation #zb_to_spawn {ns}.data *= #zb_player_count {ns}.data
execute if score #zb_to_spawn {ns}.data matches 257.. run scoreboard players set #zb_to_spawn {ns}.data 256

# Snapshot the round's total zombie count (zb_to_spawn is decremented as they spawn).
# Used by the power-up drop chance: min(5%, 2/total_round_zombies).
scoreboard players operation #zb_round_total {ns}.data = #zb_to_spawn {ns}.data

# Calculate initial spawn timer and batch size for this round
function {ns}:v{version}/zombies/calc_spawn_timer

# Grace period: don't check game over for 3 seconds (60 ticks)
scoreboard players set #zb_round_grace {ns}.data 60

# Reset stuck zombie glow timers
scoreboard players set #zb_stuck_timer {ns}.data 0
scoreboard players set #zb_glow_timer {ns}.data 0

# Signal round start
function #{ns}:zombies/on_round_start

# Refresh sidebar
function {ns}:v{version}/zombies/refresh_sidebar

# Announce
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"red"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" has begun!","color":"red"}}]
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/round_start_generic ambient @s ~ ~ ~ 0.3 1.0
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
# Tag unlocked zombie spawns near any alive player (shared 32->64->any helper). On return,
# #zb_near_found is 0 iff nothing was tagged, so no global @e existence scan is needed here.
function {ns}:v{version}/zombies/tag_spawns_near_players

# Activation-box gating: a spawn that defines an activation box is only usable while an alive
# player stands inside that box. Drop box-gated candidates whose box is currently empty.
execute as @e[tag={ns}.zb_near] if data entity @s data.abox run function {ns}:v{version}/zombies/filter_spawn_abox

# Pick random from tagged set and spawn
execute as @n[tag={ns}.zb_near,sort=random] at @s run function {ns}:v{version}/zombies/do_spawn_zombie

# Cleanup
tag @e[tag={ns}.zb_near] remove {ns}.zb_near
""")

	## Shared spawn-proximity tagger: tag unlocked zombie spawn markers into {ns}.zb_near, choosing the
	## closest available ring to any alive in-game player (32 -> 64 -> any unlocked fallback). Reused by
	## round spawning AND stuck-zombie rescue so the selection logic lives in exactly one place.
	##
	## Each radius pass dispatches a per-player subfunction that records — via its own `tag` command's
	## result — whether it tagged anything, summed into #zb_near_found. This replaces the old global
	## `unless entity @e[tag={ns}.zb_near]` existence checks (a full entity scan each) with a free score
	## compare. (You cannot `store` the aggregate on the `as @a ... run tag` line directly: `store` keeps
	## only the last iteration, so the subfunction is what lets each player OR its success into the score.)
	## On return #zb_near_found is 0 iff zb_near is empty, so callers can gate on it without any @e scan.
	## Assumes zb_near is clean on entry — every caller clears it after consuming the tagged set.
	write_versioned_function("zombies/tag_spawns_near_players", f"""
scoreboard players set #zb_near_found {ns}.data 0

# First pass: 32 blocks from any alive player
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/tag_zb_near_32

# Second pass: 64 blocks if none found
execute if score #zb_near_found {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/tag_zb_near_64

# Fallback: any unlocked spawn. `store success` so #zb_near_found also reflects the fallback,
# letting callers gate "did we tag anything at all" purely on the score.
execute if score #zb_near_found {ns}.data matches 0 store success score #zb_near_found {ns}.data run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked] add {ns}.zb_near
""")

	## Per-player spawn-tagging passes. @s = an alive in-game player, executed at their position.
	## #zb_near_hit = how many markers THIS player newly tagged; accumulated into #zb_near_found so
	## the caller can tell whether any player tagged a spawn without a global @e scan.
	write_versioned_function("zombies/tag_zb_near_32", f"""
execute store result score #zb_near_hit {ns}.data run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked,distance=..32] add {ns}.zb_near
scoreboard players operation #zb_near_found {ns}.data += #zb_near_hit {ns}.data
""")
	write_versioned_function("zombies/tag_zb_near_64", f"""
execute store result score #zb_near_hit {ns}.data run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked,distance=..64] add {ns}.zb_near
scoreboard players operation #zb_near_found {ns}.data += #zb_near_hit {ns}.data
""")

	## Activation-box filter (runs as a candidate spawn marker that has data.abox).
	## Removes the marker from the candidate set unless an alive in-game player is inside its box.
	write_versioned_function("zombies/filter_spawn_abox", f"""
data modify storage {ns}:temp _abox_chk set from entity @s data.abox
scoreboard players set #abox_ok {ns}.data 0
function {ns}:v{version}/zombies/test_spawn_abox with storage {ns}:temp _abox_chk
execute if score #abox_ok {ns}.data matches 0 run tag @s remove {ns}.zb_near
""")

	## Macro: set #abox_ok to 1 if any alive in-game player is within the absolute box volume.
	write_versioned_function("zombies/test_spawn_abox", f"""
$execute if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,x=$(x),y=$(y),z=$(z),dx=$(dx),dy=$(dy),dz=$(dz)] run scoreboard players set #abox_ok {ns}.data 1
""")

	## Actually spawn the zombie at the marker position (@s = spawn marker, at @s)
	write_versioned_function("zombies/do_spawn_zombie", f"""
# Determine zombie level based on round
# Rounds 1-5: level 1, 6-10: level 2, 11-15: level 3, 16+: level 4
execute if score #zb_round {ns}.data matches ..5 run data modify storage {ns}:temp _zpos.level set value "1"
execute if score #zb_round {ns}.data matches 6..10 run data modify storage {ns}:temp _zpos.level set value "2"
execute if score #zb_round {ns}.data matches 11..15 run data modify storage {ns}:temp _zpos.level set value "3"
execute if score #zb_round {ns}.data matches 16.. run data modify storage {ns}:temp _zpos.level set value "4"

# Zombie type: special types ("armed", "fast", "tank") are Zonweeb-only once implemented;
# the Vanilla variant must always spawn "normal" zombies.
data modify storage {ns}:temp _zpos.type set value "normal"

# Spawn the zombie (~ ~ ~ is spawn marker position, inherited from at @s in spawn_zombie)
function {ns}:v{version}/zombies/summon_zombie_at with storage {ns}:temp _zpos

# Remember which spawn point (@s) this zombie used, so a stuck-rescue never reuses it
scoreboard players operation @n[tag={ns}.zombie_round,tag={ns}.zb_rising] {ns}.zb.spawn.sid = @s {ns}.zb.spawn.sid
""")

	## Summon zombie at execution position (macro for level/type dispatch)
	# Uses ~ ~-2 ~ so zombie spawns 2 blocks underground for the rise animation.
	# Execution context comes from: spawn_zombie → at @s (spawn marker) → do_spawn_zombie → here.
	write_versioned_function("zombies/summon_zombie_at", f"""
# Summon zombie 2 blocks underground with NoAI (rise animation in progress)
# Attach a marker passenger so death can be intercepted before vanilla event 60 (poof particles).
# follow_range drives BOTH target acquisition AND the pathfinding region/node budget
# (region radius = follow_range+16, nodes = follow_range*16). A huge value (2048) made every
# repath build a multi-thousand-block region and explore 32k+ nodes, so paths failed and zombies
# froze. A sane value (40, just above vanilla's 35) keeps pathfinding cheap and reliable; long-range
# targeting is unnecessary because zombies spawn next to players and stuck ones are teleport-rescued.
summon minecraft:zombie ~ ~-2 ~ {{Tags:["{ns}.zombie_round","{ns}.gm_entity","{ns}.nukable","{ns}.zb_rising"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty",NoAI:1b,Silent:1b,Passengers:[{{id:"minecraft:marker",Tags:["{ns}.death_watch","{ns}.gm_entity"]}}],Attributes:[{{id:"minecraft:follow_range",base:40.0d}}]}}

# Apply type-specific scaling (health, speed, rise timer)
$execute as @n[tag={ns}.zombie_round,tag=!{ns}.zb_scaled] run function {ns}:v{version}/zombies/types/$(type) {{level:"$(level)"}}

# Initialize stuck detection scores (timestamp + XZ snapshot + distance bucket at spawn)
execute as @n[tag={ns}.zombie_round,tag={ns}.zb_rising] run scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
execute as @n[tag={ns}.zombie_round,tag={ns}.zb_rising] store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag={ns}.zombie_round,tag={ns}.zb_rising] store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @n[tag={ns}.zombie_round,tag={ns}.zb_rising] {ns}.zb.stuck_dist 4
""")

	# Enemy Types ───────────────────────────────────────────────
	# Each type function receives {level:"1"|"2"|"3"|"4"} as macro argument.
	# All types call the shared scale logic; stubs fall through to normal scaling.

	## Normal zombie: scale health/speed by level + start rise animation
	write_versioned_function("zombies/types/normal", f"""
# Add scaled tag, and few data
tag @s add {ns}.zb_scaled
data modify entity @s DeathTime set value -16s

# Compute round-scaled HP (base_health * 1.1^(round - 1)) and apply it to this zombie
function {ns}:v{version}/zombies/calc_zombie_hp
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp {ns}.data
function {ns}:v{version}/zombies/apply_zombie_hp with storage {ns}:temp _zb_hp

# Explicit speed per round, capped at 0.32 from round 13+
execute if score #zb_round {ns}.data matches 1 run attribute @s minecraft:movement_speed base set 0.20
execute if score #zb_round {ns}.data matches 2 run attribute @s minecraft:movement_speed base set 0.21
execute if score #zb_round {ns}.data matches 3 run attribute @s minecraft:movement_speed base set 0.22
execute if score #zb_round {ns}.data matches 4 run attribute @s minecraft:movement_speed base set 0.23
execute if score #zb_round {ns}.data matches 5 run attribute @s minecraft:movement_speed base set 0.24
execute if score #zb_round {ns}.data matches 6 run attribute @s minecraft:movement_speed base set 0.25
execute if score #zb_round {ns}.data matches 7 run attribute @s minecraft:movement_speed base set 0.26
execute if score #zb_round {ns}.data matches 8 run attribute @s minecraft:movement_speed base set 0.27
execute if score #zb_round {ns}.data matches 9 run attribute @s minecraft:movement_speed base set 0.28
execute if score #zb_round {ns}.data matches 10 run attribute @s minecraft:movement_speed base set 0.29
execute if score #zb_round {ns}.data matches 11 run attribute @s minecraft:movement_speed base set 0.30
execute if score #zb_round {ns}.data matches 12 run attribute @s minecraft:movement_speed base set 0.31
execute if score #zb_round {ns}.data matches 13.. run attribute @s minecraft:movement_speed base set 0.32

# For round 15+, 10% walkers (0.20 speed)
execute if score #zb_round {ns}.data matches 15.. store result score #zb_speed_roll {ns}.data run random value 1..10
execute if score #zb_round {ns}.data matches 15.. if score #zb_speed_roll {ns}.data matches 1 run attribute @s minecraft:movement_speed base set 0.20

# Fixed melee damage: 15.0 HP = 7.5 hearts and no knockback
attribute @s minecraft:attack_damage base set 15.0
attribute @s minecraft:knockback_resistance base set 1024

# Start rise animation (20 ticks to rise 2 blocks)
scoreboard players set @s {ns}.zb.rise_tick 20
""")

	## Compute zombie HP for current round: health = base_health * 1.1^(round - 1)
	## base_health = 20 (vanilla zombie HP, i.e. BO2's 150 HP scaled by 2/15 to Minecraft scale)
	write_versioned_function("zombies/calc_zombie_hp", f"""
# Exponent: round - 1
scoreboard players operation #zb_exp_round {ns}.data = #zb_round {ns}.data
scoreboard players remove #zb_exp_round {ns}.data 1

# 1.1^(round - 1)
data modify storage bs:in math.pow.x set value 1.1f
execute store result storage bs:in math.pow.y float 1 run scoreboard players get #zb_exp_round {ns}.data
function #bs.math:pow

# health = base_health (20) * 1.1^(round - 1)
execute store result score #zb_hp {ns}.data run data get storage bs:out math.pow 20

# Cap at Minecraft-safe gameplay max
execute unless score #zb_hp {ns}.data matches 15..2048 run scoreboard players set #zb_hp {ns}.data 2048
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

# Check if a power-up should drop at this zombie's position.
function {ns}:v{version}/zombies/powerups/check_drop

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

# Announce
execute store result score #completed_round {ns}.data run data get storage {ns}:zombies game.round
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"green"}},{{"score":{{"name":"#completed_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" complete! Next round in 5 seconds...","color":"green"}}]
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/round_end_generic ambient @s ~ ~ ~ 0.3 1.0

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

	# Managed Horde Ambience ─────────────────────────────────────
	# Round zombies are summoned Silent (no per-entity vanilla sounds), so a 50-zombie horde
	# can't stack into an ear-splitting wall of groans. Instead, each player periodically hears
	# ONE controlled groan whose volume scales gently with the nearby zombie count and is hard
	# capped — a full horde sounds full without blowing out the player's ears.
	write_versioned_function("zombies/horde_ambient", f"""
# @s = an in-game player. Count zombies within earshot.
execute store result score #horde_count {ns}.data if entity @e[tag={ns}.zombie_round,distance=..32]
execute if score #horde_count {ns}.data matches ..0 run return 0

# Volume (hundredths) = 0.25 + count*0.03, hard-capped at 0.80 (so ~18+ zombies all sound the same).
scoreboard players set #horde_vol {ns}.data 25
scoreboard players operation #horde_tmp {ns}.data = #horde_count {ns}.data
scoreboard players operation #horde_tmp {ns}.data *= #3 {ns}.data
scoreboard players operation #horde_vol {ns}.data += #horde_tmp {ns}.data
execute if score #horde_vol {ns}.data matches 80.. run scoreboard players set #horde_vol {ns}.data 80

# Random pitch 0.70..1.05 for variety so the loop doesn't sound metronomic.
execute store result score #horde_pitch {ns}.data run random value 70..105

# Hand volume/pitch to the macro as doubles (value/100).
execute store result storage {ns}:temp _horde.vol double 0.01 run scoreboard players get #horde_vol {ns}.data
execute store result storage {ns}:temp _horde.pitch double 0.01 run scoreboard players get #horde_pitch {ns}.data

# Play the groan FROM a random nearby zombie's position (positional audio), so the player hears
# the horde coming from the right direction/distance rather than centred on themselves.
execute at @e[tag={ns}.zombie_round,distance=..32,sort=random,limit=1] run function {ns}:v{version}/zombies/horde_ambient_play with storage {ns}:temp _horde
""")

	# @s = the player; execution position = a nearby zombie, so the sound is directional.
	write_versioned_function("zombies/horde_ambient_play", "$playsound minecraft:entity.zombie.ambient hostile @s ~ ~ ~ $(vol) $(pitch)")

	## Hook death watch + horde ambience into the main zombies game tick
	write_versioned_function("zombies/game_tick", f"""
# Intercept dying zombies before vanilla death particles are emitted.
function {ns}:v{version}/zombies/death_watch_tick

# Managed horde ambience: ~every 35 ticks, give each player one controlled, count-scaled groan.
scoreboard players add #zb_horde_timer {ns}.data 1
execute if score #zb_horde_timer {ns}.data matches 35.. run scoreboard players set #zb_horde_timer {ns}.data 0
execute if score #zb_horde_timer {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/horde_ambient
""")

	## Cleanup for round/end bulk-kill paths
	write_versioned_function("zombies/stop", f"""
kill @e[type=minecraft:marker,tag={ns}.death_watch]
""")
