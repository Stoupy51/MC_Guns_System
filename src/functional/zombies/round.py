
# ruff: noqa: E501
# Zombies Round System
# Wave-based round progression with zombie spawning, scaling, and round completion.
from stewbeet import Mem, write_function, write_versioned_function

from ..helpers import MGS_TAG


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

# Dog round: every 5th round from 5 on, and only on maps that placed special spawn markers
scoreboard players set #zb_dog_round {ns}.data 0
scoreboard players operation #zb_dog_mod {ns}.data = #zb_round {ns}.data
scoreboard players operation #zb_dog_mod {ns}.data %= #5 {ns}.data
execute if score #zb_has_special {ns}.data matches 1 if score #zb_round {ns}.data matches 5.. if score #zb_dog_mod {ns}.data matches 0 run scoreboard players set #zb_dog_round {ns}.data 1

# Player count, clamped at 4, drives both round-size formulas
execute store result score #zb_player_count {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
execute if score #zb_player_count {ns}.data matches 5.. run scoreboard players set #zb_player_count {ns}.data 4

# Enemy count for this round — see each subfunction for its curve
execute if score #zb_dog_round {ns}.data matches 0 run function {ns}:v{version}/zombies/calc_round_count_zombies
execute if score #zb_dog_round {ns}.data matches 1 run function {ns}:v{version}/zombies/calc_round_count_dogs

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

# Reset the freeze watchdog: its counter survives between matches and would trip recovery early
scoreboard players set #zb_wd_ticks {ns}.data 0

# Signal round start
function #{ns}:zombies/on_round_start

# Refresh sidebar
function {ns}:v{version}/zombies/refresh_sidebar

# Announce
execute if score #zb_dog_round {ns}.data matches 0 run tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"red"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" has begun!","color":"red"}}]
execute if score #zb_dog_round {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/round_start_generic ambient @s ~ ~ ~ 0.15 1.0

# Dog rounds get their own announcement + howl instead of the usual round jingle
execute if score #zb_dog_round {ns}.data matches 1 run tellraw @a ["",{{"text":"","color":"dark_red","bold":true}},"🐺 ",{{"text":"Round ","color":"dark_red"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" — the hounds are loose!","color":"dark_red"}}]
execute if score #zb_dog_round {ns}.data matches 1 as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound minecraft:entity.wolf.howl ambient @s ~ ~ ~ 1.0 0.6
""")

	## Standard round size: min(256, min(96, 7 + round) * min(4, player_count))
	# Solo player: r1=8,  r5=12, r10=17, r20=27,  r40=47,  r41+ caps at 96
	# 4+ players:  r1=32, r5=48, r10=68, r20=108, r40=188, r41+ caps at 256
	write_versioned_function("zombies/calc_round_count_zombies", f"""
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players add #zb_to_spawn {ns}.data 7
execute if score #zb_to_spawn {ns}.data matches 97.. run scoreboard players set #zb_to_spawn {ns}.data 96
scoreboard players operation #zb_to_spawn {ns}.data *= #zb_player_count {ns}.data
execute if score #zb_to_spawn {ns}.data matches 257.. run scoreboard players set #zb_to_spawn {ns}.data 256
""")

	## Dog round size: min(48, min(12, 4 + round/3) * min(4, player_count)).
	# Far below the zombie curve on purpose: short frantic bursts, not another attrition wave.
	# Solo player: r5=5,  r10=7,  r20=10, r25+ caps at 12
	# 4+ players:  r5=20, r10=28, r20=40, r25+ caps at 48
	write_versioned_function("zombies/calc_round_count_dogs", f"""
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data /= #3 {ns}.data
scoreboard players add #zb_to_spawn {ns}.data 4
execute if score #zb_to_spawn {ns}.data matches 13.. run scoreboard players set #zb_to_spawn {ns}.data 12
scoreboard players operation #zb_to_spawn {ns}.data *= #zb_player_count {ns}.data
execute if score #zb_to_spawn {ns}.data matches 49.. run scoreboard players set #zb_to_spawn {ns}.data 48

# Concurrent pack size: BO sends hounds in packs of 2-4 scaled by players, refilled as they die,
# rather than releasing the round's whole count at once. Solo 3 -> 4 players 6.
scoreboard players operation #zb_dog_cap {ns}.data = #zb_player_count {ns}.data
scoreboard players add #zb_dog_cap {ns}.data 2

# Arm this round's guaranteed Max Ammo
scoreboard players set #zb_dog_ammo_done {ns}.data 0
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

# Dog rounds ignore the zombie curve entirely: flat 1s between hounds, with the concurrency cap in
# spawn_dog_capped doing the real pacing. The zombie formula bottoms out at 1 tick / batch 2 by
# round 20, which dumped a whole pack in a single second.
execute if score #zb_dog_round {ns}.data matches 1 run scoreboard players set #zb_spawn_timer {ns}.data 20
execute if score #zb_dog_round {ns}.data matches 1 run scoreboard players set #zb_spawn_batch {ns}.data 1
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
	##
	## Generated per marker kind — zombie spawns and the special spawns dog rounds draw from. The
	## two paths differ only in the marker tag, so the ring logic stays written once.
	for kind, marker_tag, entry_point in (
		("zb", f"{ns}.spawn_zb", "zombies/tag_spawns_near_players"),
		("special", f"{ns}.spawn_special", "zombies/tag_special_spawns_near_players"),
	):
		write_versioned_function(entry_point, f"""
scoreboard players set #zb_near_found {ns}.data 0

# First pass: 32 blocks from any alive player
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/tag_{kind}_near_32

# Second pass: 64 blocks if none found
execute if score #zb_near_found {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/tag_{kind}_near_64

# Fallback: any unlocked spawn. `store success` so #zb_near_found also reflects the fallback,
# letting callers gate "did we tag anything at all" purely on the score.
execute if score #zb_near_found {ns}.data matches 0 store success score #zb_near_found {ns}.data run tag @e[tag={marker_tag},tag={ns}.spawn_unlocked] add {ns}.zb_near
""")

		## Per-player spawn-tagging passes. @s = an alive in-game player, executed at their position.
		## #zb_near_hit = how many markers THIS player newly tagged; accumulated into #zb_near_found so
		## the caller can tell whether any player tagged a spawn without a global @e scan.
		write_versioned_function(f"zombies/tag_{kind}_near_32", f"""
execute store result score #zb_near_hit {ns}.data run tag @e[tag={marker_tag},tag={ns}.spawn_unlocked,distance=..32] add {ns}.zb_near
scoreboard players operation #zb_near_found {ns}.data += #zb_near_hit {ns}.data
""")
		write_versioned_function(f"zombies/tag_{kind}_near_64", f"""
execute store result score #zb_near_hit {ns}.data run tag @e[tag={marker_tag},tag={ns}.spawn_unlocked,distance=..64] add {ns}.zb_near
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

	## Release one hound, unless the pack is already at full strength. Skipping without touching
	## #zb_to_spawn leaves it queued for the next timer tick, so the round still spawns its full
	## count — it just refills the pack as hounds die instead of dumping them all at once.
	write_versioned_function("zombies/spawn_dog_capped", f"""
scoreboard players operation #zb_dog_live {ns}.data = #zb_alive {ns}.data
scoreboard players operation #zb_dog_live {ns}.data += #zb_dog_pending {ns}.data
execute if score #zb_dog_live {ns}.data >= #zb_dog_cap {ns}.data run return 0

function {ns}:v{version}/zombies/spawn_dog
scoreboard players remove #zb_to_spawn {ns}.data 1
""")

	## Spawn a single dog, mirroring spawn_zombie but drawing from the special spawn markers.
	write_versioned_function("zombies/spawn_dog", f"""
# Tag unlocked special spawns near any alive player (32->64->any helper)
function {ns}:v{version}/zombies/tag_special_spawns_near_players

# Activation-box gating works exactly as it does for zombie spawns.
execute as @e[tag={ns}.zb_near] if data entity @s data.abox run function {ns}:v{version}/zombies/filter_spawn_abox

# Pick random from tagged set and spawn
execute as @n[tag={ns}.zb_near,sort=random] at @s run function {ns}:v{version}/zombies/do_spawn_dog

# Cleanup
tag @e[tag={ns}.zb_near] remove {ns}.zb_near
""")

	## Open a spawn portal at the marker position (@s = special spawn marker, at @s).
	## Dogs don't rise from the ground like zombies: BO2-style, the spot sparks for 1.5s and then a
	## lightning strike delivers the dog. This marker is the sparking phase.
	write_versioned_function("zombies/do_spawn_dog", f"""
summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.dog_portal","{ns}.gm_entity"]}}

# 30 ticks (1.5s) of telegraph before the strike
scoreboard players set @n[tag={ns}.dog_portal,tag=!{ns}.dog_portal_armed] {ns}.zb.rise_tick 30

# Carry the spawn point id through, so a stuck-rescue never reuses the spawn the dog came from
scoreboard players operation @n[tag={ns}.dog_portal,tag=!{ns}.dog_portal_armed] {ns}.zb.spawn.sid = @s {ns}.zb.spawn.sid
tag @n[tag={ns}.dog_portal,tag=!{ns}.dog_portal_armed] add {ns}.dog_portal_armed

# A telegraphing dog isn't an entity yet, so #zb_alive can't see it — count it or the round
# completes early with the last dog still mid-portal (see game_tick).
scoreboard players add #zb_dog_pending {ns}.data 1

# Opening cue: a crackle at the strike point. Volume 2.0 = 32 blocks of reach to match the
# selector, with a minVolume floor so the telegraph carries to players further out.
playsound minecraft:block.beacon.deactivate weather @a[distance=..32] ~ ~ ~ 2.0 1.9 0.25
""")

	## Per-tick telegraph: sparks gathering at the strike point, counting down to the bolt.
	write_versioned_function("zombies/dog_portal_tick", f"""
particle minecraft:electric_spark ~ ~0.3 ~ 0.25 0.4 0.25 0.06 4 normal @a[distance=..48]
particle minecraft:crit ~ ~0.1 ~ 0.3 0.05 0.3 0.02 2 normal @a[distance=..32]

scoreboard players remove @s {ns}.zb.rise_tick 1
execute if score @s {ns}.zb.rise_tick matches ..0 run function {ns}:v{version}/zombies/dog_portal_strike
""")

	## The bolt lands: flash + thunder, then the dog. Deliberately NOT a lightning_bolt entity — that
	## would ignite the map, shock players and traders, and carry its thunder dimension-wide.
	write_versioned_function("zombies/dog_portal_strike", f"""
# flash is a ColorParticleOption type, so the ARGB color is mandatory. Cold blue-white.
particle minecraft:flash{{color:[1.0f,0.82f,0.90f,1.0f]}} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..64]
particle minecraft:electric_spark ~ ~1.2 ~ 0.25 1.4 0.25 0.35 70 force @a[distance=..48]
particle minecraft:end_rod ~ ~1 ~ 0.1 0.8 0.1 0.02 12 force @a[distance=..48]
# weather category: where lightning belongs, and a slider players rarely turn down (hostile is
# commonly lowered to mute zombie groans).
# Volume sets the audible RADIUS (1.0 = 16 blocks), not loudness, so it has to cover the selector
# range or distant players are targeted but hear nothing. The trailing minVolume is the floor
# players outside that radius still hear, so a hound spawning across the map is never silent.
playsound minecraft:entity.lightning_bolt.impact weather @a[distance=..48] ~ ~ ~ 3.0 1.2 0.5
playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..64] ~ ~ ~ 4.0 1.5 0.4

# Same level buckets as zombies, so the type dispatch signature stays uniform
execute if score #zb_round {ns}.data matches ..5 run data modify storage {ns}:temp _zpos.level set value "1"
execute if score #zb_round {ns}.data matches 6..10 run data modify storage {ns}:temp _zpos.level set value "2"
execute if score #zb_round {ns}.data matches 11..15 run data modify storage {ns}:temp _zpos.level set value "3"
execute if score #zb_round {ns}.data matches 16.. run data modify storage {ns}:temp _zpos.level set value "4"
function {ns}:v{version}/zombies/summon_dog_at with storage {ns}:temp _zpos

# Hand the spawn point id over to the dog, then retire the portal
scoreboard players operation @n[tag={ns}.zb_dog_new] {ns}.zb.spawn.sid = @s {ns}.zb.spawn.sid
tag @n[tag={ns}.zb_dog_new] remove {ns}.zb_dog_new
scoreboard players remove #zb_dog_pending {ns}.data 1
kill @s
""")

	## Summon dog at execution position (macro for level dispatch)
	# Wolves carry {ns}.zombie_round like every other enemy, so alive counts, round completion, traps,
	# barriers, nukes and the stuck-rescue all apply with no extra wiring. Unlike zombies they are NOT
	# Silent — a pack is small enough that its own growls are the ambience (horde_ambient is skipped).
	write_versioned_function("zombies/summon_dog_at", f"""
# Delivered by the bolt at ground level, AI live immediately — no rise animation, so no zb_rising.
# zb_dog_new is a scratch tag the strike removes once setup is done.
summon minecraft:wolf ~ ~ ~ {{Tags:["{ns}.zombie_round","{ns}.zb_dog","{ns}.zb_dog_new","{ns}.gm_entity","{ns}.nukable"],variant:"minecraft:black",PersistenceRequired:true,DeathLootTable:"minecraft:empty",Passengers:[{{id:"minecraft:marker",Tags:["{ns}.death_watch","{ns}.gm_entity"]}}],Attributes:[{{id:"minecraft:follow_range",base:40.0d}}]}}

# Apply level scaling (health, speed)
$execute as @n[tag={ns}.zb_dog_new] run function {ns}:v{version}/zombies/types/dog {{level:"$(level)"}}

# Ally with escort traders, same reason as zombies (escort.py)
team join {ns}.horde @n[tag={ns}.zb_dog_new]

# Initialize stuck detection scores (timestamp + XZ snapshot + distance bucket at spawn)
execute as @n[tag={ns}.zb_dog_new] run scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
execute as @n[tag={ns}.zb_dog_new] store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag={ns}.zb_dog_new] store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @n[tag={ns}.zb_dog_new] {ns}.zb.stuck_dist 4
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

# Ally with escort traders (escort.py: forCombat targeting fails between allies, so the trader
# never flees the horde and zombies never attack the pathfinding taxi)
team join {ns}.horde @n[tag={ns}.zombie_round,tag={ns}.zb_rising]

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

# Compute round-scaled HP (BO1 curve: +100 BO-HP per round until R9, then x1.1 per round) and apply it to this zombie
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

	## Compute zombie HP for current round, using the classic Treyarch (BO1) two-phase curve:
	##   Rounds 1-9:  bo_hp = 50 + 100 * round        (R1=150, R2=250, ..., R9=950)
	##   Round 10+:   bo_hp = 950 * 1.1^(round - 9)   (R10=1045, R11=1150, ...)
	## BO HP is then converted to Minecraft scale with a 2/15 factor (BO 150 HP = MC 20 HP, vanilla zombie)
	write_versioned_function("zombies/calc_zombie_hp", f"""
# Rounds 1-9: bo_hp = 50 + 100 * round
execute if score #zb_round {ns}.data matches ..9 run scoreboard players operation #zb_hp {ns}.data = #zb_round {ns}.data
execute if score #zb_round {ns}.data matches ..9 run scoreboard players operation #zb_hp {ns}.data *= #100 {ns}.data
execute if score #zb_round {ns}.data matches ..9 run scoreboard players add #zb_hp {ns}.data 50

# Round 10+: exponent = round - 9
execute if score #zb_round {ns}.data matches 10.. run scoreboard players operation #zb_exp_round {ns}.data = #zb_round {ns}.data
execute if score #zb_round {ns}.data matches 10.. run scoreboard players remove #zb_exp_round {ns}.data 9

# Round 10+: bo_hp = 950 * 1.1^(round - 9)
execute if score #zb_round {ns}.data matches 10.. run data modify storage bs:in math.pow.x set value 1.1f
execute if score #zb_round {ns}.data matches 10.. store result storage bs:in math.pow.y float 1 run scoreboard players get #zb_exp_round {ns}.data
execute if score #zb_round {ns}.data matches 10.. run function #bs.math:pow
execute if score #zb_round {ns}.data matches 10.. store result score #zb_hp {ns}.data run data get storage bs:out math.pow 950

# Convert BO HP to Minecraft scale: hp = bo_hp * 2 / 15 (R1: 150 -> 20 HP)
scoreboard players operation #zb_hp {ns}.data *= #2 {ns}.data
scoreboard players operation #zb_hp {ns}.data /= #15 {ns}.data

# Cap at Minecraft-safe gameplay max (also catches int overflow on very high rounds)
execute unless score #zb_hp {ns}.data matches 15..2048 run scoreboard players set #zb_hp {ns}.data 2048
""")

	## Apply computed HP to the current zombie (@s)
	write_versioned_function("zombies/apply_zombie_hp", """
$attribute @s minecraft:max_health base set $(val)
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get
""")

	## Dog: fast, tanky, hits hard. 1.5x the round's zombie HP — at 60% a sniper one-shot them on the
	## early dog rounds, which made a pack trivial. They still die faster in practice than the number
	## suggests, since they close to melee range where every weapon connects.
	write_versioned_function("zombies/types/dog", f"""
# Add scaled tag, and few data
tag @s add {ns}.zb_scaled
data modify entity @s DeathTime set value -16s

# 150% of the round's zombie HP, floored at 2x a vanilla zombie so round 5 dogs aren't one-shot
function {ns}:v{version}/zombies/calc_zombie_hp
scoreboard players operation #zb_hp {ns}.data *= #3 {ns}.data
scoreboard players operation #zb_hp {ns}.data /= #2 {ns}.data
execute if score #zb_hp {ns}.data matches ..39 run scoreboard players set #zb_hp {ns}.data 40
execute if score #zb_hp {ns}.data matches 2049.. run scoreboard players set #zb_hp {ns}.data 2048
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp {ns}.data
function {ns}:v{version}/zombies/apply_zombie_hp with storage {ns}:temp _zb_hp

# Always faster than the zombie cap (0.32) — outrunning a dog pack should not be an option
execute if score #zb_round {ns}.data matches ..9 run attribute @s minecraft:movement_speed base set 0.36
execute if score #zb_round {ns}.data matches 10..19 run attribute @s minecraft:movement_speed base set 0.40
execute if score #zb_round {ns}.data matches 20.. run attribute @s minecraft:movement_speed base set 0.44

# Slightly below zombie melee (15.0), because dogs reach you far more often
attribute @s minecraft:attack_damage base set 12.0
attribute @s minecraft:knockback_resistance base set 1024

# Hellhound build: 1.5x a vanilla wolf, which also scales the hitbox so they're easier to hit
attribute @s minecraft:scale base set 1.5
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

# Check if a power-up should drop at this zombie's position. Dogs never roll the random table — a
# dog round's only drop is the guaranteed Max Ammo from the last hound.
execute unless entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/powerups/check_drop

# Dogs: handle the death separately, since "was this the last one" needs an exact count.
execute if entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/dog_death

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

# Dog rounds spawn one hound per timer tick, capped by how many are already out
execute if score #zb_dog_round {ns}.data matches 1 run return run function {ns}:v{version}/zombies/spawn_dog_capped

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

# Dog rounds always end with a Max Ammo. Normally the last hound already dropped it as it died;
# this only covers the cases where that path didn't fire.
execute if score #zb_dog_round {ns}.data matches 1 if score #zb_dog_ammo_done {ns}.data matches 0 run function {ns}:v{version}/zombies/dog_max_ammo_fallback

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

	## Dog death. #zb_alive is the wrong thing to test here: it only counts materialized dogs, so once
	## #zb_to_spawn hits 0 with portals still telegraphing it reads 1 while several hounds are still
	## inbound — which made each of the last few kills look like "the last one". Count the live pack
	## directly instead, after dropping this corpse out of it, and add the portals that haven't struck.
	write_versioned_function("zombies/dog_death", f"""
tag @s remove {ns}.zb_dog

scoreboard players operation #zb_dog_left {ns}.data = #zb_dog_pending {ns}.data
scoreboard players operation #zb_dog_left {ns}.data += #zb_to_spawn {ns}.data
execute store result score #zb_dog_alive {ns}.data if entity @e[tag={ns}.zb_dog]
scoreboard players operation #zb_dog_left {ns}.data += #zb_dog_alive {ns}.data

# ammo_done also covers the same-tick case: two hounds dying together both see the pack empty.
execute if score #zb_dog_left {ns}.data matches ..0 if score #zb_dog_ammo_done {ns}.data matches 0 run function {ns}:v{version}/zombies/dog_max_ammo_at_self
""")

	## Primary path: @s is the last hound, still standing where it died. Bypasses the shuffle bag and
	## drop roll — it's a fixed reward, so it calls the per-type spawner directly.
	write_versioned_function("zombies/dog_max_ammo_at_self", f"""
scoreboard players set #zb_dog_ammo_done {ns}.data 1
scoreboard players add #pu_uid {ns}.data 1
data modify storage {ns}:temp _pu_spawn set value {{x:0,y:0,z:0,uid:0}}
data modify storage {ns}:temp _pu_spawn.x set from entity @s Pos[0]
data modify storage {ns}:temp _pu_spawn.y set from entity @s Pos[1]
data modify storage {ns}:temp _pu_spawn.z set from entity @s Pos[2]
execute store result storage {ns}:temp _pu_spawn.uid int 1 run scoreboard players get #pu_uid {ns}.data
function {ns}:v{version}/zombies/powerups/spawn_type/max_ammo with storage {ns}:temp _pu_spawn
""")

	## Fallback, for a dog round that ends without any hound running the at-death path — a Nuke, or a
	## death that skipped the death watch. Drops at a player rather than at a remembered position:
	## a stored position is what let a stale record pay out a second time at an earlier dog's corpse.
	write_versioned_function("zombies/dog_max_ammo_fallback", f"""
execute as @r[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/dog_max_ammo_at_self
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

	# Freeze Watchdog ────────────────────────────────────────────
	# A round advances through one handoff chain: spawn -> die -> round_complete -> (5s) ->
	# start_round. Any link can go missing (function that failed to load, schedule dropped on
	# /reload, desynced counter, spawn pass that tagged nothing) and the match then sits at
	# "0 zombies" forever. Rather than enumerating those, watch the property they all share:
	# nothing alive, nothing queued, nothing changing — impossible during real play, where the
	# longest legitimate pause is the 5s handoff.
	write_versioned_function("zombies/watchdog_tick", f"""
# Progress fingerprint: any spawn, kill, or portal strike moves it.
scoreboard players operation #zb_wd_fp {ns}.data = #zb_alive {ns}.data
scoreboard players operation #zb_wd_fp {ns}.data += #zb_to_spawn {ns}.data
scoreboard players operation #zb_wd_fp {ns}.data += #zb_dog_pending {ns}.data

# Anything alive counts as progress on its own: kiting a horde is a normal, arbitrarily long state,
# and unreachable zombies are already handled by the stuck escort/glow system.
scoreboard players set #zb_wd_moved {ns}.data 0
execute if score #zb_alive {ns}.data matches 1.. run scoreboard players set #zb_wd_moved {ns}.data 1
execute unless score #zb_wd_fp {ns}.data = #zb_wd_last {ns}.data run scoreboard players set #zb_wd_moved {ns}.data 1
scoreboard players operation #zb_wd_last {ns}.data = #zb_wd_fp {ns}.data

execute if score #zb_wd_moved {ns}.data matches 1 run scoreboard players set #zb_wd_ticks {ns}.data 0
execute if score #zb_wd_moved {ns}.data matches 0 run scoreboard players add #zb_wd_ticks {ns}.data 1

# 400 ticks = 20s, well past the 5s handoff so a healthy round can't trip it.
execute if score #zb_wd_ticks {ns}.data matches 400.. run function {ns}:zombies/recover
""")

	## Rebuild a frozen round. Also the manual escape hatch (admin button / typed in chat), so a
	## stuck game never needs a restart — version-less so it stays typeable without the pack version.
	write_function(f"{ns}:zombies/recover", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]

scoreboard players set #zb_wd_ticks {ns}.data 0

# Blockers that hold a round open without showing in the sidebar: a desynced dog-portal counter,
# and portals that never struck (their dogs are lost either way).
scoreboard players set #zb_dog_pending {ns}.data 0
kill @e[tag={ns}.dog_portal]

# Drop any handoff still in flight so recovery can't race a schedule landing a tick later
schedule clear {ns}:v{version}/zombies/start_round

tellraw @a [{MGS_TAG},{{"text":"Round was frozen — recovering.","color":"yellow"}}]

# Case A: round_complete ran (it parks #zb_to_spawn at -1) but start_round never landed
execute if score #zb_to_spawn {ns}.data matches ..-1 run return run function {ns}:v{version}/zombies/start_round

# Case B: map empty and nothing queued, but the round never closed — close it
kill @e[tag={ns}.zombie_round]
scoreboard players set #zb_to_spawn {ns}.data 0
function {ns}:v{version}/zombies/round_complete
""")

	## Hook death watch + horde ambience into the main zombies game tick
	write_versioned_function("zombies/game_tick", f"""
# Intercept dying zombies before vanilla death particles are emitted.
function {ns}:v{version}/zombies/death_watch_tick

# Freeze watchdog: auto-recover a round that has stopped advancing (see watchdog_tick).
function {ns}:v{version}/zombies/watchdog_tick

# Dog spawn portals: 1.5s of sparks, then the bolt. Gated on the round kind, NOT on
# #zb_dog_pending — a portal orphaned by a desynced counter would then never tick, never strike and
# never die, which is the freeze the resync in game_tick pairs with this to rule out.
execute if score #zb_dog_round {ns}.data matches 1 as @e[tag={ns}.dog_portal] at @s run function {ns}:v{version}/zombies/dog_portal_tick

# Wolves are neutral mobs and hunt nothing without an anger target. Writing `angry_at` alone is
# enough (the game calls setTarget() from it on reload, then sustains the timer); writing AngerTime
# does nothing, as the always-saved `anger_end_time` outranks it. The `unless data` guard means a
# dog already locked on costs a read and no write. #zb_tick_mod is total_tick % 20 from earlier.
execute if score #zb_dog_round {ns}.data matches 1 if score #zb_tick_mod {ns}.data matches 0 as @e[tag={ns}.zb_dog,tag=!{ns}.zb_rising] at @s unless data entity @s angry_at run data modify entity @s angry_at set from entity @p[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,gamemode=!creative] UUID

# Managed horde ambience: ~every 35 ticks, give each player one controlled, count-scaled groan.
# Skipped on dog rounds: dogs aren't summoned Silent, so their own growls are the ambience.
scoreboard players add #zb_horde_timer {ns}.data 1
execute if score #zb_horde_timer {ns}.data matches 35.. run scoreboard players set #zb_horde_timer {ns}.data 0
execute if score #zb_dog_round {ns}.data matches 0 if score #zb_horde_timer {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/horde_ambient
""")

	## Cleanup for round/end bulk-kill paths
	write_versioned_function("zombies/stop", f"""
kill @e[type=minecraft:marker,tag={ns}.death_watch]

# Portals are gm_entity so the bulk cleanup already removes them; the counter they feed has to be
# zeroed by hand or a stale value would block the next game's round completion forever.
kill @e[type=minecraft:marker,tag={ns}.dog_portal]
scoreboard players set #zb_dog_pending {ns}.data 0
""")
