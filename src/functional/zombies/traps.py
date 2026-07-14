
# ruff: noqa: E501
# Trap System
# Area-of-effect devices that damage zombies in a radius for a duration, then enter cooldown.
# Type 0 = fire: lethal to zombies (1000% of max health), 5 fire damage to players inside.
# Type 1 = electric: lethal to zombies (1000% of max health), 5 electric damage to players inside.
# Type 2 = turret: shoots the nearest zombie in range every 5 ticks for 45% of its max health;
#          the bullet stops at the first entity hit, so players between the turret and zombies take 2 damage instead.
from stewbeet import JsonDict, Mem, Predicate, set_json_encoder, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from .common import deny_not_enough_points_body, deny_requires_power_body, game_active_guard_cmd


def generate_traps() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Predicate: does `this` entity's trap id match the turret currently being processed?
	## Used to select the matching head/interaction by score directly in a selector (predicate=...),
	## which is cheaper than `execute as @e[...] if score @s ... = #turret_tid ...`.
	id_ref: JsonDict = {"type": "minecraft:score", "target": {"type": "minecraft:fixed", "name": "#turret_tid"}, "score": f"{ns}.data"}
	Mem.ctx.data[ns].predicates[f"v{version}/zombies/traps/turret_id_match"] = set_json_encoder(Predicate({
		"condition": "minecraft:entity_scores",
		"entity": "this",
		"scores": {f"{ns}.zb.trap.id": {"min": id_ref, "max": id_ref}},
	}), max_level=-1)

	## Trap entity scoreboards
	write_load_file(f"""
# Trap entity scoreboards
scoreboard objectives add {ns}.zb.trap.id dummy
scoreboard objectives add {ns}.zb.trap.price dummy
scoreboard objectives add {ns}.zb.trap.power dummy
scoreboard objectives add {ns}.zb.trap.type dummy
scoreboard objectives add {ns}.zb.trap.dur dummy
scoreboard objectives add {ns}.zb.trap.cd_max dummy
scoreboard objectives add {ns}.zb.trap.timer dummy
scoreboard objectives add {ns}.zb.trap.cd dummy
scoreboard objectives add {ns}.zb.trap.rx dummy
scoreboard objectives add {ns}.zb.trap.ry dummy
scoreboard objectives add {ns}.zb.trap.rz dummy
""")

	## Setup: iterate trap compounds, summon interaction + marker entities
	write_versioned_function("zombies/traps/setup", f"""
scoreboard players set #trap_counter {ns}.data 0
data modify storage {ns}:temp _trap_iter set from storage {ns}:zombies game.map.traps
execute if data storage {ns}:temp _trap_iter[0] run function {ns}:v{version}/zombies/traps/setup_iter
""")

	write_versioned_function("zombies/traps/setup_iter", f"""
# Assign incrementing ID
scoreboard players add #trap_counter {ns}.data 1

# Read interaction position (relative) and convert to absolute
execute store result score #tix {ns}.data run data get storage {ns}:temp _trap_iter[0].pos[0]
execute store result score #tiy {ns}.data run data get storage {ns}:temp _trap_iter[0].pos[1]
execute store result score #tiz {ns}.data run data get storage {ns}:temp _trap_iter[0].pos[2]
scoreboard players operation #tix {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #tiy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #tiz {ns}.data += #gm_base_z {ns}.data

# Compute trap effect center from interaction position + offset_pos
execute store result score #tx {ns}.data run data get storage {ns}:temp _trap_iter[0].offset_pos[0]
execute store result score #ty {ns}.data run data get storage {ns}:temp _trap_iter[0].offset_pos[1]
execute store result score #tz {ns}.data run data get storage {ns}:temp _trap_iter[0].offset_pos[2]
scoreboard players operation #tx {ns}.data += #tix {ns}.data
scoreboard players operation #ty {ns}.data += #tiy {ns}.data
scoreboard players operation #tz {ns}.data += #tiz {ns}.data

# Store positions for macros
execute store result storage {ns}:temp _trap.cx int 1 run scoreboard players get #tx {ns}.data
execute store result storage {ns}:temp _trap.cy int 1 run scoreboard players get #ty {ns}.data
execute store result storage {ns}:temp _trap.cz int 1 run scoreboard players get #tz {ns}.data
execute store result storage {ns}:temp _trap.ix int 1 run scoreboard players get #tix {ns}.data
execute store result storage {ns}:temp _trap.iy int 1 run scoreboard players get #tiy {ns}.data
execute store result storage {ns}:temp _trap.iz int 1 run scoreboard players get #tiz {ns}.data

# Summon entities
function {ns}:v{version}/zombies/traps/place_at with storage {ns}:temp _trap

# Set scoreboards on interaction entity (type is also stored here for the hover text)
scoreboard players operation @n[tag={ns}._trap_new_i] {ns}.zb.trap.id = #trap_counter {ns}.data
execute store result score @n[tag={ns}._trap_new_i] {ns}.zb.trap.price run data get storage {ns}:temp _trap_iter[0].price
execute store result score @n[tag={ns}._trap_new_i] {ns}.zb.trap.power run data get storage {ns}:temp _trap_iter[0].power
execute store result score @n[tag={ns}._trap_new_i] {ns}.zb.trap.type run data get storage {ns}:temp _trap_iter[0].type
tag @e[tag={ns}._trap_new_i] remove {ns}._trap_new_i

# Set scoreboards on marker entity
scoreboard players operation @n[tag={ns}._trap_new_m] {ns}.zb.trap.id = #trap_counter {ns}.data
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.type run data get storage {ns}:temp _trap_iter[0].type
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.dur run data get storage {ns}:temp _trap_iter[0].duration
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.cd_max run data get storage {ns}:temp _trap_iter[0].cooldown
scoreboard players set @n[tag={ns}._trap_new_m] {ns}.zb.trap.timer 0
scoreboard players set @n[tag={ns}._trap_new_m] {ns}.zb.trap.cd 0

# Store per-axis effect radius
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.rx run data get storage {ns}:temp _trap_iter[0].effect_radius[0]
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.ry run data get storage {ns}:temp _trap_iter[0].effect_radius[1]
execute store result score @n[tag={ns}._trap_new_m] {ns}.zb.trap.rz run data get storage {ns}:temp _trap_iter[0].effect_radius[2]
tag @e[tag={ns}._trap_new_m] remove {ns}._trap_new_m

# Register Bookshelf events on interaction entity
execute as @e[tag={ns}._trap_new_bs] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/traps/on_right_click",executor:"source"}}
execute as @e[tag={ns}._trap_new_bs] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/traps/on_hover",executor:"source"}}
tag @e[tag={ns}._trap_new_bs] remove {ns}._trap_new_bs

# Turret traps (type 2) get a visible two-part model: a stationary base + a head that aims at its
# target. The head carries this trap's id so turret_fire can find and rotate the matching head.
execute store result score #trap_type {ns}.data run data get storage {ns}:temp _trap_iter[0].type
data modify storage {ns}:temp _trap.yaw set value 0.0f
execute if data storage {ns}:temp _trap_iter[0].rotation[0] run data modify storage {ns}:temp _trap.yaw set from storage {ns}:temp _trap_iter[0].rotation[0]
execute if score #trap_type {ns}.data matches 2 run function {ns}:v{version}/zombies/traps/place_turret_at with storage {ns}:temp _trap
execute if score #trap_type {ns}.data matches 2 run scoreboard players operation @n[tag={ns}._trap_new_head] {ns}.zb.trap.id = #trap_counter {ns}.data
execute if score #trap_type {ns}.data matches 2 run tag @e[tag={ns}._trap_new_head] remove {ns}._trap_new_head

# Continue iteration
data remove storage {ns}:temp _trap_iter[0]
execute if data storage {ns}:temp _trap_iter[0] run function {ns}:v{version}/zombies/traps/setup_iter
""")

	write_versioned_function("zombies/traps/place_at", f"""
# Summon interaction entity centred on the block, at the floor. height:-2.0 makes a downward 2-block
# hitbox; setup_iter then raises it 2 blocks (tp ~ ~2 ~) so it covers the 2-block turret from the floor
# up - the same trick the perk machine uses.
$execute positioned $(ix) $(iy) $(iz) run summon minecraft:interaction ~ ~2 ~ {{width:1.1f,height:-2.0f,response:true,Tags:["{ns}.trap_interact","{ns}.gm_entity","bs.entity.interaction","{ns}._trap_new_i","{ns}._trap_new_bs"]}}

# Summon marker entity at trap center
$summon minecraft:marker $(cx) $(cy) $(cz) {{Tags:["{ns}.trap_center","{ns}.gm_entity","{ns}._trap_new_m"]}}
""")

	## Turret model: a stationary base + an aiming head. Both models are built around the origin
	## (the head around its mount/pivot), so the displays are simply summoned at their real world
	## position with an identity transform - no translation offsets. The base sits at the block centre
	## on the floor; the head's mount sits ~1.625 up so it seats in the base's yoke (yoke at 1.5..1.75),
	## and the head pivots about its own mount when aimed. teleport_duration smooths the re-aim rotation.
	write_versioned_function("zombies/traps/place_turret_at", f"""
$execute positioned $(cx) $(cy) $(cz) run summon minecraft:item_display ~ ~.5 ~ {{Rotation:[$(yaw)f,0f],Tags:["{ns}.trap_base","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:iron_block",count:1,components:{{"minecraft:item_model":"{ns}:turret_base"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2f,2f,2f]}}}}
$execute positioned $(cx) $(cy) $(cz) positioned ~ ~1.625 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw)f,0f],Tags:["{ns}.trap_head","{ns}.gm_entity","{ns}._trap_new_head"],item_display:"fixed",billboard:"fixed",teleport_duration:5,item:{{id:"minecraft:netherite_block",count:1,components:{{"minecraft:item_model":"{ns}:turret_head"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}}}
""")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/traps/on_right_click", f"""
# Guard: game must be active
{game_active_guard_cmd(ns)}

# Check power requirement
execute store result score #trap_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.power
execute if score #trap_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 run return run function {ns}:v{version}/zombies/traps/deny_requires_power

# Get trap ID
execute store result score #trap_id {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.id

# Check if trap is ready (not active, not on cooldown)
scoreboard players set #trap_ready {ns}.data 0
execute as @e[tag={ns}.trap_center] if score @s {ns}.zb.trap.id = #trap_id {ns}.data if score @s {ns}.zb.trap.timer matches 0 unless score @s {ns}.zb.trap.cd > #total_tick {ns}.data run scoreboard players set #trap_ready {ns}.data 1
execute unless score #trap_ready {ns}.data matches 1 run return run function {ns}:v{version}/zombies/traps/deny_not_ready

# Check price
execute store result score #trap_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.price
execute unless score @s {ns}.zb.points >= #trap_price {ns}.data run return run function {ns}:v{version}/zombies/traps/deny_not_enough_points

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #trap_price {ns}.data

# Activate trap (set timer = duration on the marker)
execute as @e[tag={ns}.trap_center] if score @s {ns}.zb.trap.id = #trap_id {ns}.data run scoreboard players operation @s {ns}.zb.trap.timer = @s {ns}.zb.trap.dur

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Trap activated for ","color":"gold"}},{{"score":{{"name":"#trap_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points.","color":"gold"}}]
function {ns}:v{version}/zombies/feedback/sound_announce
""")

	write_versioned_function("zombies/traps/deny_requires_power", f"""
{deny_requires_power_body(ns, version, "trap")}
""")

	write_versioned_function("zombies/traps/deny_not_ready", f"""
tellraw @s [{MGS_TAG},{{"text":"Trap is on cooldown and not ready yet.","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/traps/deny_not_enough_points", f"""
{deny_not_enough_points_body(ns, version, "#trap_price")}
""")

	## Active trap tick: damage zombies, particles, decrement timer
	write_versioned_function("zombies/traps/active_tick", f"""
# @s = trap center marker, at @s position

# Apply damage based on trap type
data modify storage {ns}:temp _trap_tick set value {{rx:0,ry:0,rz:0,sx:0,sy:0,sz:0}}
execute store result storage {ns}:temp _trap_tick.rx int 1 run scoreboard players get @s {ns}.zb.trap.rx
execute store result storage {ns}:temp _trap_tick.ry int 1 run scoreboard players get @s {ns}.zb.trap.ry
execute store result storage {ns}:temp _trap_tick.rz int 1 run scoreboard players get @s {ns}.zb.trap.rz

scoreboard players operation #trap_sx {ns}.data = @s {ns}.zb.trap.rx
scoreboard players operation #trap_sy {ns}.data = @s {ns}.zb.trap.ry
scoreboard players operation #trap_sz {ns}.data = @s {ns}.zb.trap.rz
scoreboard players operation #trap_sx {ns}.data += #trap_sx {ns}.data
scoreboard players operation #trap_sy {ns}.data += #trap_sy {ns}.data
scoreboard players operation #trap_sz {ns}.data += #trap_sz {ns}.data
execute store result storage {ns}:temp _trap_tick.sx int 1 run scoreboard players get #trap_sx {ns}.data
execute store result storage {ns}:temp _trap_tick.sy int 1 run scoreboard players get #trap_sy {ns}.data
execute store result storage {ns}:temp _trap_tick.sz int 1 run scoreboard players get #trap_sz {ns}.data

execute if score @s {ns}.zb.trap.type matches 0 run function {ns}:v{version}/zombies/traps/damage_fire with storage {ns}:temp _trap_tick
execute if score @s {ns}.zb.trap.type matches 1 run function {ns}:v{version}/zombies/traps/damage_electric with storage {ns}:temp _trap_tick

# Turret: fire a shot every 5 ticks at the nearest zombie in range
scoreboard players operation #turret_mod {ns}.data = @s {ns}.zb.trap.timer
scoreboard players operation #turret_mod {ns}.data %= #5 {ns}.data
execute if score #turret_mod {ns}.data matches 0 if score @s {ns}.zb.trap.type matches 2 run function {ns}:v{version}/zombies/traps/turret_fire with storage {ns}:temp _trap_tick

# Particles based on type
execute if score @s {ns}.zb.trap.type matches 0 run particle minecraft:flame ~ ~1 ~ 1.5 0.5 1.5 0.05 10
execute if score @s {ns}.zb.trap.type matches 1 run particle minecraft:electric_spark ~ ~1 ~ 1.5 0.5 1.5 0.1 15
execute if score @s {ns}.zb.trap.type matches 2 run particle minecraft:smoke ~ ~1 ~ 0.2 0.2 0.2 0.01 2

# Decrement timer
scoreboard players remove @s {ns}.zb.trap.timer 1

# Check if deactivated: set cooldown as expiration tick
execute if score @s {ns}.zb.trap.timer matches 0 run scoreboard players operation @s {ns}.zb.trap.cd = @s {ns}.zb.trap.cd_max
execute if score @s {ns}.zb.trap.timer matches 0 run scoreboard players operation @s {ns}.zb.trap.cd += #total_tick {ns}.data
""")

	write_versioned_function("zombies/traps/damage_fire", f"""
# Zombies: lethal damage (1000% of each zombie's max health)
data modify storage {ns}:temp _trap_dmg.type set value "minecraft:on_fire"
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag={ns}.zombie_round,dx=$(sx),dy=$(sy),dz=$(sz)] run function {ns}:v{version}/zombies/traps/kill_zombie

# Players inside the trap: 5 fire damage
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @a[scores={{{ns}.zb.in_game=1}},gamemode=!creative,gamemode=!spectator,dx=$(sx),dy=$(sy),dz=$(sz)] run damage @s 5 minecraft:on_fire
""")

	write_versioned_function("zombies/traps/damage_electric", f"""
# Zombies: lethal damage (1000% of each zombie's max health)
data modify storage {ns}:temp _trap_dmg.type set value "minecraft:lightning_bolt"
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag={ns}.zombie_round,dx=$(sx),dy=$(sy),dz=$(sz)] run function {ns}:v{version}/zombies/traps/kill_zombie

# Players inside the trap: 5 electric damage
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @a[scores={{{ns}.zb.in_game=1}},gamemode=!creative,gamemode=!spectator,dx=$(sx),dy=$(sy),dz=$(sz)] run damage @s 5 minecraft:lightning_bolt
""")

	## Per-zombie lethal damage: 1000% of this zombie's max health (damage type set by caller in _trap_dmg.type)
	write_versioned_function("zombies/traps/kill_zombie", f"""
execute store result storage {ns}:temp _trap_dmg.amount int 1 run attribute @s minecraft:max_health get 10
function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _trap_dmg
""")

	write_versioned_function("zombies/traps/apply_trap_damage", """
$damage @s $(amount) $(type)
""")

	## Turret trap: pick the nearest *visible* zombie in the effect box, aim the head at it, then fire a bullet
	write_versioned_function("zombies/traps/turret_fire", f"""
# @s = trap center marker, at @s position
# Remember this trap's id so we can find/rotate the matching head display and use it as the muzzle
scoreboard players operation #turret_tid {ns}.data = @s {ns}.zb.trap.id

# Tag every zombie inside the effect box as a candidate, keep only those the head has line of sight to,
# then pick the one nearest the turret center
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag={ns}.zombie_round,tag=!{ns}.zb_rising,dx=$(sx),dy=$(sy),dz=$(sz)] run tag @s add {ns}._turret_cand
execute as @e[tag={ns}._turret_cand] run function {ns}:v{version}/zombies/traps/turret_check_los
# Capture, via the tag command's success, whether a target was selected — avoids the global
# `unless entity @e[tag={ns}._turret_target]` scan below. limit=1 means this runs at most once;
# #turret_has_target stays 0 if there was no visible zombie (the body never executes).
scoreboard players set #turret_has_target {ns}.data 0
execute as @e[tag={ns}._turret_visible,sort=nearest,limit=1] store success score #turret_has_target {ns}.data run tag @s add {ns}._turret_target
tag @e[tag={ns}._turret_cand] remove {ns}._turret_cand
tag @e[tag={ns}._turret_visible] remove {ns}._turret_visible

# No visible zombie in range: nothing to aim at or shoot
execute if score #turret_has_target {ns}.data matches 0 run return 0

# Aim this turret's head display at the target (yaw + pitch via facing entity, smoothed by teleport_duration)
execute as @e[tag={ns}.trap_head,predicate={ns}:v{version}/zombies/traps/turret_id_match] at @s run tp @s ~ ~ ~ facing entity @n[tag={ns}._turret_target] eyes

# Fire the bullet straight from the head display itself (no manual offset) toward the target
execute as @e[tag={ns}.trap_head,predicate={ns}:v{version}/zombies/traps/turret_id_match] at @s facing entity @n[tag={ns}._turret_target] eyes positioned ^ ^ ^1 run function {ns}:v{version}/zombies/traps/turret_shoot

# Clear the temporary target tag
tag @e[tag={ns}._turret_target] remove {ns}._turret_target
""")

	## Line-of-sight gate: tag the candidate zombie as visible only if the turret can see it.
	## can_see_ata raycasts from the execution position to @s (the zombie), returning 1 if unobstructed.
	## The turret head sits half inside a barrier block, so casting from there would self-block; instead we
	## cast from 1.5 blocks below the interaction entity (clear of the barrier) - matched by id via predicate.
	write_versioned_function("zombies/traps/turret_check_los", f"""
# @s = candidate zombie
scoreboard players set #turret_vis {ns}.data 0
execute at @e[tag={ns}.trap_interact,predicate={ns}:v{version}/zombies/traps/turret_id_match] positioned ~ ~-1.5 ~ store result score #turret_vis {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #turret_vis {ns}.data matches 1 run tag @s add {ns}._turret_visible
""")

	## Fire the turret bullet: raycast that stops at the first entity hit
	write_versioned_function("zombies/traps/turret_shoot", f"""
# @s = trap center marker (execution position = turret muzzle, facing the target)
# Tracer particle + G3A3 gunshot (close report + 'large' acoustics crack, same as a player firing a G3A3)
particle minecraft:crit ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[distance=..64]
function {ns}:v{version}/sound/turret_fire

# Raycast with piercing 0: the ray stops at the first entity hit,
# so a player standing between the turret and the zombies takes the bullet instead
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage {ns}:input with.entities set value "!global.ignore"
data modify storage {ns}:input with.piercing set value 0
data modify storage {ns}:input with.max_distance set value 32
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/empty"
data modify storage {ns}:input with.ignored_entities set value "#{ns}:ignore"
data modify storage {ns}:input with.on_targeted_entity set value "function {ns}:v{version}/zombies/traps/turret_hit"
function #bs.raycast:run with storage {ns}:input
""")

	## Turret bullet impact (@s = hit entity, positioned at the hit point)
	write_versioned_function("zombies/traps/turret_hit", f"""
# Impact particles
particle minecraft:crit ~ ~1 ~ 0.2 0.3 0.2 0.1 8 force @a[distance=..48]

# Zombie hit: 45% of its max health
execute if entity @s[tag={ns}.zombie_round] store result storage {ns}:temp _trap_dmg.amount int 1 run attribute @s minecraft:max_health get 0.45
execute if entity @s[tag={ns}.zombie_round] run data modify storage {ns}:temp _trap_dmg.type set value "{ns}:bullet"
execute if entity @s[tag={ns}.zombie_round] run return run function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _trap_dmg

# Player caught between the turret and the zombies: 2 damage
execute if entity @s[type=player,gamemode=!creative,gamemode=!spectator] if score @s {ns}.zb.in_game matches 1.. run damage @s 2 {ns}:bullet
""")

	## Hover events (executor: "source" = player)
	write_versioned_function("zombies/traps/on_hover", f"""
execute store result score #trap_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.price
execute store result score #trap_type {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.type
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚠ Trap","color":"red"}},{{"text":" - Cost: ","color":"gray"}},{{"score":{{"name":"#trap_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}],priority:"conditional",freeze:5}}
execute if score #trap_type {ns}.data matches 0 run data modify storage smithed.actionbar:input message.json[0] set value {{"text":"🔥 Fire Trap","color":"red"}}
execute if score #trap_type {ns}.data matches 1 run data modify storage smithed.actionbar:input message.json[0] set value {{"text":"⚡ Electric Trap","color":"aqua"}}
execute if score #trap_type {ns}.data matches 2 run data modify storage smithed.actionbar:input message.json[0] set value {{"text":"🔫 Turret Trap","color":"gold"}}
function #smithed.actionbar:message
""")

	## Hook into game tick: process active traps and cooldowns
	write_versioned_function("zombies/game_tick", f"""
# Trap active tick (damage + timer)
execute as @e[tag={ns}.trap_center,scores={{{ns}.zb.trap.timer=1..}}] at @s run function {ns}:v{version}/zombies/traps/active_tick
""")

	## Hook into preload_complete: setup traps
	write_versioned_function("zombies/preload_complete", f"""
# Setup traps
execute if data storage {ns}:zombies game.map.traps[0] run function {ns}:v{version}/zombies/traps/setup
""")

