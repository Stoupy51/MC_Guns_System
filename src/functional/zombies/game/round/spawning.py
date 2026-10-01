""" Spawn pacing, proximity marker selection, activation boxes and the dog spawn portals. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_round_spawning() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Spawn timer max(1, 20 - round) ticks, batch floor((round - 1) / 50) + 1.
	write_versioned_function("zombies/calc_spawn_timer", f"""
scoreboard players set #zb_spawn_timer {ns}.data 20
scoreboard players operation #zb_spawn_timer {ns}.data -= #zb_round {ns}.data
execute if score #zb_spawn_timer {ns}.data matches ..1 run scoreboard players set #zb_spawn_timer {ns}.data 1

scoreboard players operation #zb_spawn_batch {ns}.data = #zb_round {ns}.data
scoreboard players remove #zb_spawn_batch {ns}.data 1
scoreboard players operation #zb_spawn_batch {ns}.data /= #50 {ns}.data
scoreboard players add #zb_spawn_batch {ns}.data 1

# Dog rounds pace on the concurrency cap of spawn_dog_capped, not on the zombie curve,
# which reaches 1 tick by round 20 and would release a whole pack in one second.
execute if score #zb_dog_round {ns}.data matches 1 run scoreboard players set #zb_spawn_timer {ns}.data 20
execute if score #zb_dog_round {ns}.data matches 1 run scoreboard players set #zb_spawn_batch {ns}.data 1
""")

	## Spawn one zombie at a random unlocked spawn near a player.
	write_versioned_function("zombies/spawn_zombie", f"""
# On return #zb_near_found is 0 if nothing was tagged.
function {ns}:v{version}/zombies/tag_spawns_near_players

# A spawn with an activation box is only usable while an alive player stands in that box.
execute as @e[tag={ns}.zb_near] if data entity @s data.abox run function {ns}:v{version}/zombies/filter_spawn_abox

execute as @n[tag={ns}.zb_near,sort=random] at @s run function {ns}:v{version}/zombies/do_spawn_zombie

tag @e[tag={ns}.zb_near] remove {ns}.zb_near
""")

	# Tag the unlocked spawns of one marker kind closest to any alive player (within 32, else 64, else any); callers leave zb_near empty.
	# Each player's pass adds what it tagged to #zb_near_found, since `store` on an `as @a` line keeps only the last iteration.
	for kind, marker_tag, entry_point in (
		("zb", f"{ns}.spawn_zb", "zombies/tag_spawns_near_players"),
		("special", f"{ns}.spawn_special", "zombies/tag_special_spawns_near_players"),
	):
		write_versioned_function(entry_point, f"""
scoreboard players set #zb_near_found {ns}.data 0

execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/tag_{kind}_near_32

execute if score #zb_near_found {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/tag_{kind}_near_64

# `store success` so #zb_near_found also reflects the fallback.
execute if score #zb_near_found {ns}.data matches 0 store success score #zb_near_found {ns}.data run tag @e[tag={marker_tag},tag={ns}.spawn_unlocked] add {ns}.zb_near
""")

		## Run as an alive in-game player, at their position.
		write_versioned_function(f"zombies/tag_{kind}_near_32", f"""
execute store result score #zb_near_hit {ns}.data run tag @e[tag={marker_tag},tag={ns}.spawn_unlocked,distance=..32] add {ns}.zb_near
scoreboard players operation #zb_near_found {ns}.data += #zb_near_hit {ns}.data
""")
		write_versioned_function(f"zombies/tag_{kind}_near_64", f"""
execute store result score #zb_near_hit {ns}.data run tag @e[tag={marker_tag},tag={ns}.spawn_unlocked,distance=..64] add {ns}.zb_near
scoreboard players operation #zb_near_found {ns}.data += #zb_near_hit {ns}.data
""")

	## Run as a candidate spawn with data.abox: drop it unless an alive player is inside the box.
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

	## Run as the spawn marker, at it.
	write_versioned_function("zombies/do_spawn_zombie", f"""
# Level: rounds 1-5 give 1, 6-10 give 2, 11-15 give 3, 16+ give 4.
execute if score #zb_round {ns}.data matches ..5 run data modify storage {ns}:temp _zpos.level set value "1"
execute if score #zb_round {ns}.data matches 6..10 run data modify storage {ns}:temp _zpos.level set value "2"
execute if score #zb_round {ns}.data matches 11..15 run data modify storage {ns}:temp _zpos.level set value "3"
execute if score #zb_round {ns}.data matches 16.. run data modify storage {ns}:temp _zpos.level set value "4"

# Special types ("armed", "fast", "tank") are for Zonweeb; Vanilla always spawns "normal".
data modify storage {ns}:temp _zpos.type set value "normal"

function {ns}:v{version}/zombies/summon_zombie_at with storage {ns}:temp _zpos

# Remembered so a stuck-rescue never reuses this spawn.
scoreboard players operation @n[tag={ns}.zb_new] {ns}.zb.spawn.sid = @s {ns}.zb.spawn.sid

# Walk-to spawn (map editor `walk_to`): zombie_finish_rise walks the zombie there instead of letting it wander.
execute if data entity @s data.walk_to run data modify entity @n[tag={ns}.zb_new] data.walk_to set from entity @s data.walk_to

tag @n[tag={ns}.zb_new] remove {ns}.zb_new
""")

	## Release one hound unless the pack is full; a skipped spawn stays queued in #zb_to_spawn.
	write_versioned_function("zombies/spawn_dog_capped", f"""
scoreboard players operation #zb_dog_live {ns}.data = #zb_alive {ns}.data
scoreboard players operation #zb_dog_live {ns}.data += #zb_dog_pending {ns}.data
execute if score #zb_dog_live {ns}.data >= #zb_dog_cap {ns}.data run return 0

function {ns}:v{version}/zombies/spawn_dog
scoreboard players remove #zb_to_spawn {ns}.data 1
""")

	## Same as spawn_zombie, drawing from the special spawn markers.
	write_versioned_function("zombies/spawn_dog", f"""
function {ns}:v{version}/zombies/tag_special_spawns_near_players

execute as @e[tag={ns}.zb_near] if data entity @s data.abox run function {ns}:v{version}/zombies/filter_spawn_abox

execute as @n[tag={ns}.zb_near,sort=random] at @s run function {ns}:v{version}/zombies/do_spawn_dog

tag @e[tag={ns}.zb_near] remove {ns}.zb_near
""")

	## Run as the special spawn marker: the spot sparks for 1.5 s, then a bolt delivers the dog (BO2 style).
	write_versioned_function("zombies/do_spawn_dog", f"""
summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.dog_portal","{ns}.gm_entity"]}}

scoreboard players set @n[tag={ns}.dog_portal,tag=!{ns}.dog_portal_armed] {ns}.zb.rise_tick 30

scoreboard players operation @n[tag={ns}.dog_portal,tag=!{ns}.dog_portal_armed] {ns}.zb.spawn.sid = @s {ns}.zb.spawn.sid
tag @n[tag={ns}.dog_portal,tag=!{ns}.dog_portal_armed] add {ns}.dog_portal_armed

# A dog still in its portal is not an entity, so count it or the round ends early (see game_tick).
scoreboard players add #zb_dog_pending {ns}.data 1

# Volume 2.0 reaches the 32-block selector; minVolume lets players further out hear it.
playsound minecraft:block.beacon.deactivate ambient @a[distance=..32] ~ ~ ~ 2.0 1.9 0.25
""")

	## Telegraph in 3 escalating phases so the strike point reads from across the map.
	write_versioned_function("zombies/dog_portal_tick", f"""
# Phase 1 (30 ticks): a ring on the floor marks the footprint.
particle minecraft:electric_spark ~ ~0.1 ~ 1.1 0.02 1.1 0.0 5 force @a[distance=..48]

# Phase 2 (last 20): the charge climbs out of the floor.
execute if score @s {ns}.zb.rise_tick matches ..20 run particle minecraft:electric_spark ~ ~0.7 ~ 0.35 0.9 0.35 0.03 8 force @a[distance=..48]

# Phase 3 (last 10): a column forms and the ring tightens.
execute if score @s {ns}.zb.rise_tick matches ..10 run particle minecraft:end_rod ~ ~1.2 ~ 0.12 1.3 0.12 0.01 5 force @a[distance=..48]
execute if score @s {ns}.zb.rise_tick matches ..10 run particle minecraft:crit ~ ~0.2 ~ 0.45 0.08 0.45 0.06 8 force @a[distance=..32]

# Crackle every 5 ticks, with the same volume rule as the strike.
scoreboard players operation #zb_portal_mod {ns}.data = @s {ns}.zb.rise_tick
scoreboard players operation #zb_portal_mod {ns}.data %= #5 {ns}.data
execute if score #zb_portal_mod {ns}.data matches 0 run playsound minecraft:block.amethyst_block.resonate ambient @a[distance=..32] ~ ~ ~ 2.0 0.6 0.3

scoreboard players remove @s {ns}.zb.rise_tick 1
execute if score @s {ns}.zb.rise_tick matches ..0 run function {ns}:v{version}/zombies/dog_portal_strike
""")

	## The strike. Not a lightning_bolt entity, which would ignite the map, shock players and carry its thunder dimension-wide.
	write_versioned_function("zombies/dog_portal_strike", f"""
# A wide Y spread with near-zero XZ spread and speed 0 draws a vertical shaft.
particle minecraft:electric_spark ~ ~4 ~ 0.06 4.0 0.06 0.0 160 force @a[distance=..64]
particle minecraft:end_rod ~ ~4 ~ 0.04 4.0 0.04 0.0 40 force @a[distance=..64]

# flash takes a mandatory ARGB color.
particle minecraft:flash{{color:[1.0f,0.82f,0.90f,1.0f]}} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..64]

particle minecraft:electric_spark ~ ~0.15 ~ 1.6 0.02 1.6 0.5 90 force @a[distance=..48]
particle minecraft:crit ~ ~0.15 ~ 1.2 0.02 1.2 0.3 30 force @a[distance=..48]
playsound minecraft:entity.lightning_bolt.impact ambient @a[distance=..48] ~ ~ ~ 3.0 1.2 0.5
playsound minecraft:entity.lightning_bolt.thunder ambient @a[distance=..64] ~ ~ ~ 4.0 1.5 0.4

function {ns}:v{version}/zombies/summon_dog_at

scoreboard players operation @n[tag={ns}.zb_dog_new] {ns}.zb.spawn.sid = @s {ns}.zb.spawn.sid
tag @n[tag={ns}.zb_dog_new] remove {ns}.zb_dog_new
scoreboard players remove #zb_dog_pending {ns}.data 1
kill @s
""")

	## Wolves carry zombie_round, so round counts, traps, barricades, nukes and stuck-rescue apply to them.
	## Unlike zombies they are not Silent: a small pack's growls are the ambience.
	write_versioned_function("zombies/summon_dog_at", f"""
# Delivered at ground level with AI on, so no rise and no zb_rising; the strike removes the scratch tag zb_dog_new.
# step_height 1.0 as in summon_zombie_at; Wolf.applyTamingSideEffects only resets MAX_HEALTH, so a base value is safe here.
summon minecraft:wolf ~ ~ ~ {{Tags:["{ns}.zombie_round","{ns}.zb_dog","{ns}.zb_dog_new","{ns}.gm_entity","{ns}.nukable"],variant:"minecraft:black",PersistenceRequired:true,DeathLootTable:"minecraft:empty",Passengers:[{{id:"minecraft:marker",Tags:["{ns}.death_watch","{ns}.gm_entity"]}}],attributes:[{{id:"minecraft:follow_range",base:40.0d}},{{id:"minecraft:step_height",base:1.0d}}]}}

execute as @n[tag={ns}.zb_dog_new] run function {ns}:v{version}/zombies/types/dog

# Allied with escort traders (see escort).
team join {ns}.horde @n[tag={ns}.zb_dog_new]

execute as @n[tag={ns}.zb_dog_new] run scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
execute as @n[tag={ns}.zb_dog_new] store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag={ns}.zb_dog_new] store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @n[tag={ns}.zb_dog_new] {ns}.zb.stuck_dist 4
""")

	## Spawns 2 blocks underground for the rise animation; runs at the spawn marker.
	write_versioned_function("zombies/summon_zombie_at", f"""
# The marker passenger intercepts death before vanilla event 60 (poof particles).
# follow_range also sets the pathfinding region (range + 16) and node budget (range x 16); 40 keeps repaths cheap.
# step_height 1.0 makes 1-block rises walkable nodes instead of jump nodes that stall on stairs and slabs.
# zb_new names this zombie for the lines below: up to 20 rise at once from round 20, so @n[tag=zb_rising] can pick another.
summon minecraft:zombie ~ ~-2 ~ {{Tags:["{ns}.zombie_round","{ns}.gm_entity","{ns}.nukable","{ns}.zb_rising","{ns}.zb_new"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty",NoAI:1b,Silent:1b,Passengers:[{{id:"minecraft:marker",Tags:["{ns}.death_watch","{ns}.gm_entity"]}}],attributes:[{{id:"minecraft:follow_range",base:40.0d}},{{id:"minecraft:step_height",base:1.0d}}]}}

$execute as @n[tag={ns}.zb_new] run function {ns}:v{version}/zombies/types/$(type) {{level:"$(level)"}}

# Allied with escort traders, so traders do not flee the horde and zombies do not attack them (see escort).
team join {ns}.horde @n[tag={ns}.zb_new]

execute as @n[tag={ns}.zb_new] run scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
execute as @n[tag={ns}.zb_new] store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag={ns}.zb_new] store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @n[tag={ns}.zb_new] {ns}.zb.stuck_dist 4
""")

