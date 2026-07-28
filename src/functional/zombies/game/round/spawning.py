""" Spawn pacing, proximity marker selection, activation boxes and the dog spawn portals. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_round_spawning() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Calculate spawn timer and batch size based on current round Timer formula: max(1, 20 - round) → R1=38t, R10=20t, R20=1t+ Batch formula: floor((round - 1) / 50) + 1 → R1-50=1, R51-100=2, R101-150=3 ...
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

	# Shared spawn-proximity tagger: tag unlocked zombie spawn markers into {ns}.zb_near.
	# It picks the closest available ring to any alive in-game player: 32, then 64, then any unlocked one.
	# Reused by round spawning AND stuck-zombie rescue, so the selection logic lives in exactly one place.
	# Each radius pass dispatches a per-player subfunction that records whether it tagged anything.
	# Those results sum into #zb_near_found, replacing the old global existence checks with a free score compare.
	# `store` cannot aggregate on the `as @a ... run tag` line directly, since it keeps only the last iteration.
	# The subfunction is what lets each player OR its own success into the score.
	# On return #zb_near_found is 0 iff zb_near is empty, so callers can gate on it without any @e scan.
	# Assumes zb_near is clean on entry — every caller clears it after consuming the tagged set.
	# Generated per marker kind: zombie spawns, and the special spawns dog rounds draw from.
	# The two paths differ only in the marker tag, so the ring logic stays written once.
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

		## Per-player spawn-tagging passes.
		## @s = an alive in-game player, executed at their position.
	# #zb_near_hit counts the markers THIS player newly tagged, accumulated into #zb_near_found.
	# That lets the caller tell whether any player tagged a spawn without a global @e scan.
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

# Walk-to spawn (map editor "walk_to"): pass the target down to the zombie, which zombie_finish_rise
# then walks to instead of letting it wander (see escort/start_to_target)
execute if data entity @s data.walk_to run data modify entity @n[tag={ns}.zombie_round,tag={ns}.zb_rising] data.walk_to set from entity @s data.walk_to
""")

	## Release one hound, unless the pack is already at full strength.
	# Skipping without touching #zb_to_spawn leaves it queued for the next timer tick.
	# The round still spawns its full count, refilling the pack as hounds die instead of dumping them at once.
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
	## Dogs don't rise from the ground like zombies: BO2-style, the spot sparks for 1.5s and then a lightning strike delivers the dog.
	## This marker is the sparking phase.
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
playsound minecraft:block.beacon.deactivate ambient @a[distance=..32] ~ ~ ~ 2.0 1.9 0.25
""")

	## Per-tick telegraph: charge gathering at the strike point over 3 escalating phases, so the spot reads as "something lands HERE" from across the map rather than as ambient sparkle.
	write_versioned_function("zombies/dog_portal_tick", f"""
# Phase 1 (all 30 ticks): a flat ring crawling along the floor marks the footprint
particle minecraft:electric_spark ~ ~0.1 ~ 1.1 0.02 1.1 0.0 5 force @a[distance=..48]

# Phase 2 (last 20): the charge starts climbing out of the floor
execute if score @s {ns}.zb.rise_tick matches ..20 run particle minecraft:electric_spark ~ ~0.7 ~ 0.35 0.9 0.35 0.03 8 force @a[distance=..48]

# Phase 3 (last 10): a column forms and the ring tightens — the last beat before the bolt
execute if score @s {ns}.zb.rise_tick matches ..10 run particle minecraft:end_rod ~ ~1.2 ~ 0.12 1.3 0.12 0.01 5 force @a[distance=..48]
execute if score @s {ns}.zb.rise_tick matches ..10 run particle minecraft:crit ~ ~0.2 ~ 0.45 0.08 0.45 0.06 8 force @a[distance=..32]

# Charging crackle every 5 ticks. Same audible-radius rule as the strike: volume covers the
# selector range, minVolume is the floor for anyone further out.
scoreboard players operation #zb_portal_mod {ns}.data = @s {ns}.zb.rise_tick
scoreboard players operation #zb_portal_mod {ns}.data %= #5 {ns}.data
execute if score #zb_portal_mod {ns}.data matches 0 run playsound minecraft:block.amethyst_block.resonate ambient @a[distance=..32] ~ ~ ~ 2.0 0.6 0.3

scoreboard players remove @s {ns}.zb.rise_tick 1
execute if score @s {ns}.zb.rise_tick matches ..0 run function {ns}:v{version}/zombies/dog_portal_strike
""")

	## The bolt lands: flash + thunder, then the dog.
	## Deliberately NOT a lightning_bolt entity — that would ignite the map, shock players and traders, and carry its thunder dimension-wide.
	write_versioned_function("zombies/dog_portal_strike", f"""
# The bolt itself: a tall, thin column drawn in one command — a wide Y spread with near-zero XZ
# spread and speed 0, so the particles fill a vertical shaft instead of puffing outward.
particle minecraft:electric_spark ~ ~4 ~ 0.06 4.0 0.06 0.0 160 force @a[distance=..64]
particle minecraft:end_rod ~ ~4 ~ 0.04 4.0 0.04 0.0 40 force @a[distance=..64]

# flash is a ColorParticleOption type, so the ARGB color is mandatory. Cold blue-white.
particle minecraft:flash{{color:[1.0f,0.82f,0.90f,1.0f]}} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..64]

# Ground shockwave: a flat disc kicked outward along the floor where the bolt lands
particle minecraft:electric_spark ~ ~0.15 ~ 1.6 0.02 1.6 0.5 90 force @a[distance=..48]
particle minecraft:crit ~ ~0.15 ~ 1.2 0.02 1.2 0.3 30 force @a[distance=..48]
playsound minecraft:entity.lightning_bolt.impact ambient @a[distance=..48] ~ ~ ~ 3.0 1.2 0.5
playsound minecraft:entity.lightning_bolt.thunder ambient @a[distance=..64] ~ ~ ~ 4.0 1.5 0.4

function {ns}:v{version}/zombies/summon_dog_at

# Hand the spawn point id over to the dog, then retire the portal
scoreboard players operation @n[tag={ns}.zb_dog_new] {ns}.zb.spawn.sid = @s {ns}.zb.spawn.sid
tag @n[tag={ns}.zb_dog_new] remove {ns}.zb_dog_new
scoreboard players remove #zb_dog_pending {ns}.data 1
kill @s
""")

	## Summon dog at execution position (macro for level dispatch) Wolves carry {ns}.zombie_round like every other enemy, so alive counts, round completion, traps, barriers, nukes and the stuck-rescue all apply with no extra wiring.
	## Unlike zombies they are NOT Silent — a pack is small enough that its own growls are the ambience (horde_ambient is skipped).
	write_versioned_function("zombies/summon_dog_at", f"""
# Delivered by the bolt at ground level, AI live immediately — no rise animation, so no zb_rising.
# zb_dog_new is a scratch tag the strike removes once setup is done.
summon minecraft:wolf ~ ~ ~ {{Tags:["{ns}.zombie_round","{ns}.zb_dog","{ns}.zb_dog_new","{ns}.gm_entity","{ns}.nukable"],variant:"minecraft:black",PersistenceRequired:true,DeathLootTable:"minecraft:empty",Passengers:[{{id:"minecraft:marker",Tags:["{ns}.death_watch","{ns}.gm_entity"]}}],Attributes:[{{id:"minecraft:follow_range",base:40.0d}}]}}

# Apply scaling (health, speed). Not a macro call: types/dog reads #zb_round itself and never used
# the level argument, so passing one only added a way for the call to be skipped.
execute as @n[tag={ns}.zb_dog_new] run function {ns}:v{version}/zombies/types/dog

# Ally with escort traders, same reason as zombies (escort.py)
team join {ns}.horde @n[tag={ns}.zb_dog_new]

# Initialize stuck detection scores (timestamp + XZ snapshot + distance bucket at spawn)
execute as @n[tag={ns}.zb_dog_new] run scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
execute as @n[tag={ns}.zb_dog_new] store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag={ns}.zb_dog_new] store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @n[tag={ns}.zb_dog_new] {ns}.zb.stuck_dist 4
""")

	## Summon zombie at execution position (macro for level/type dispatch) Uses ~ ~-2 ~ so zombie spawns 2 blocks underground for the rise animation.
	## Execution context comes from: spawn_zombie → at @s (spawn marker) → do_spawn_zombie → here.
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

