""" Pending-click bookkeeping, burst mode and the grenade/projectile/hitscan routing. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import BURST, COOLDOWN, DAMAGE, FIRE_MODE, GRENADE_TYPE, PELLET_COUNT, PROJECTILE_SPEED


# Functions
def write_click_handling() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Handle pending clicks
	write_versioned_function("player/right_click", f"""
# Determine number of bullets to fire based on fire mode and held-click state
scoreboard players set #bullets_to_fire {ns}.data 1

# Check fire mode
execute store result score #fire_mode_is_semi {ns}.data if data storage {ns}:gun all.stats{{{FIRE_MODE}:"semi"}}
execute store result score #fire_mode_is_burst {ns}.data if data storage {ns}:gun all.stats{{{FIRE_MODE}:"burst"}}

# Semi-auto mode: block if holding (only allow single taps)
execute if score #fire_mode_is_semi {ns}.data matches 1 if score @s {ns}.held_click matches 1.. run return fail

# Burst mode: check if burst limit reached, if so block firing
execute if score #fire_mode_is_burst {ns}.data matches 1 store result score #burst_limit {ns}.data run data get storage {ns}:gun all.stats.{BURST}
execute if score #fire_mode_is_burst {ns}.data matches 1 if score @s {ns}.burst_count >= #burst_limit {ns}.data run return fail

# Burst mode: on first shot, set pending_clicks to (BURST-1) * COOLDOWN to sustain burst
execute if score #fire_mode_is_burst {ns}.data matches 1 if score @s {ns}.burst_count matches 0 run function {ns}:v{version}/player/init_burst_clicks

# Burst mode: increment counter
execute if score #fire_mode_is_burst {ns}.data matches 1 run scoreboard players add @s {ns}.burst_count 1

# Auto mode: allow continuous fire (no blocking)

# Set cooldown as expiration tick: end_tick = current_tick + cooldown_duration
execute store result score #cooldown {ns}.data run data get storage {ns}:gun all.stats.{COOLDOWN}
# Timeslip (zombies perk): halve the grenade/equipment throw cooldown for the owner (grenades only)
execute if score @s {ns}.special.timeslip matches 1 if data storage {ns}:gun all.stats.{GRENADE_TYPE} run scoreboard players operation #cooldown {ns}.data /= #2 {ns}.data
scoreboard players operation #cooldown {ns}.data += #total_tick {ns}.data
scoreboard players operation @s {ns}.cooldown = #cooldown {ns}.data

# Route to the appropriate firing method (projectile or hitscan)
function {ns}:v{version}/player/fire_weapon

# Signal: on_shoot (weapon data available in mgs:signals)
data modify storage {ns}:signals on_shoot set value {{}}
data modify storage {ns}:signals on_shoot.weapon set from storage {ns}:gun all
function #{ns}:signals/on_shoot
""")

	# Fire weapon routing: grenade vs projectile vs hitscan
	write_versioned_function("player/fire_weapon", f"""
# For weapons with pellet count, set bullets_to_fire appropriately
execute if data storage {ns}:gun all.stats.{PELLET_COUNT} store result score #bullets_to_fire {ns}.data run data get storage {ns}:gun all.stats.{PELLET_COUNT}

# Per-shot budget for entity hit particles: only the first 3 entities hit by this shot
# (all pellets included) emit blood particles, to avoid lag when piercing a whole horde
scoreboard players set #hit_particles_left {ns}.data 3

# If weapon is a grenade, throw it instead
execute if data storage {ns}:gun all.stats.{GRENADE_TYPE} run return run function {ns}:v{version}/grenade/throw

# If weapon has projectile config, fire slow projectile(s) instead of instant raycast
execute if data storage {ns}:gun all.stats.{PROJECTILE_SPEED} run return run function {ns}:v{version}/projectile/summon_loop

# Shoot with hitscan raycast
function {ns}:v{version}/player/shoot
""")

	# Initialize burst mode pending clicks
	write_versioned_function("player/init_burst_clicks", f"""
# Calculate (BURST - 1) * COOLDOWN
execute store result score #burst_clicks {ns}.data run data get storage {ns}:gun all.stats.{BURST}
scoreboard players remove #burst_clicks {ns}.data 1
execute store result score #cooldown_value {ns}.data run data get storage {ns}:gun all.stats.{COOLDOWN}
scoreboard players operation #burst_clicks {ns}.data *= #cooldown_value {ns}.data

# Set pending_clicks to sustain burst firing
scoreboard players operation @s {ns}.pending_clicks = #burst_clicks {ns}.data
""")

	# Handle pending clicks
	write_versioned_function("player/shoot", f"""
# Check which type of movement the player is doing
function {ns}:v{version}/raycast/accuracy/get_value

# Deadshot Daiquiri (zombies perk): tighten weapon spread to 65%
execute if score @s {ns}.special.deadshot matches 1 run function {ns}:v{version}/raycast/accuracy/deadshot_scale

# Shoot with raycast & launch cloud particle forward
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^2 run particle minecraft:cloud ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[tag=!bs.raycast.omit,distance=..32]
execute anchored eyes positioned ^ ^ ^ summon marker run function {ns}:v{version}/raycast/main
tag @s remove bs.raycast.omit

# Decrease bullets to fire & loop if needed
scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/player/shoot
""")

	# Handle pending clicks
	write_versioned_function("raycast/main", f"""
# Copy damage to temp storage to avoid modifying original for multiple pellets
data modify storage {ns}:temp damage set from storage {ns}:gun all.stats.{DAMAGE}

# Handle accuracy
tp @s ~ ~ ~ ~ ~
function {ns}:v{version}/raycast/accuracy/apply_spread

# Scores to remember to only play a sound type once
scoreboard players set #played_water {ns}.data 0
scoreboard players set #played_glass {ns}.data 0
scoreboard players set #played_cloth {ns}.data 0
scoreboard players set #played_dirt {ns}.data 0
scoreboard players set #played_mud {ns}.data 0
scoreboard players set #played_wood {ns}.data 0
scoreboard players set #played_plant {ns}.data 0
scoreboard players set #played_solid {ns}.data 0
scoreboard players set #played_soft {ns}.data 0
scoreboard players set #next_air_particle {ns}.data 0

# Prepare arguments
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage {ns}:input with.entities set value "!global.ignore"
data modify storage {ns}:input with.piercing set value 10
data modify storage {ns}:input with.max_distance set value 128
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/empty"
data modify storage {ns}:input with.ignored_entities set value "#{ns}:ignore"
data modify storage {ns}:input with.on_entry_point set value "function {ns}:v{version}/raycast/on_entry_point"
data modify storage {ns}:input with.on_targeted_block set value "function {ns}:v{version}/raycast/on_targeted_block"
data modify storage {ns}:input with.on_targeted_entity set value "function {ns}:v{version}/raycast/on_targeted_entity"
data modify storage {ns}:input with.on_exit_point set value "function {ns}:v{version}/raycast/on_exit_point"

# Launch raycast with callbacks (https://docs.mcbookshelf.dev/en/latest/modules/raycast.html#run-the-raycast)
execute at @s run function #bs.raycast:run with storage {ns}:input

# Kill marker
kill @s
""")

