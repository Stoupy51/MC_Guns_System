""" Pending-click bookkeeping, burst mode and the grenade/projectile/hitscan routing. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import (
	COOLDOWN,
	DAMAGE,
	FIRE_MODE,
	FIRE_MODES,
	GRENADE_TYPE,
	PELLET_COUNT,
	PROJECTILE_SPEED,
)


# Functions
def write_click_handling() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("player/right_click", f"""
# From the fire mode and the held-click state.
scoreboard players set #bullets_to_fire {ns}.data 1

execute store result score #fire_mode_is_burst {ns}.data if data storage {ns}:gun all.stats{{{FIRE_MODE}:"burst"}}

# Semi and pump: single taps only.
execute if score @s {ns}.held_click matches 1.. if data storage {ns}:gun all.stats{{{FIRE_MODE}:"semi"}} run return fail
execute if score @s {ns}.held_click matches 1.. if data storage {ns}:gun all.stats{{{FIRE_MODE}:"pump"}} run return fail

# Burst: no more once the burst limit is reached.
execute if score #fire_mode_is_burst {ns}.data matches 1 store result score #burst_limit {ns}.data run data get storage {ns}:gun all.stats.{FIRE_MODES}[0].burst
execute if score #fire_mode_is_burst {ns}.data matches 1 if score @s {ns}.burst_count >= #burst_limit {ns}.data run return fail

# The fire mode's cooldown when it has one, its Pack-a-Punch value on an upgraded gun.
execute store result score #cooldown {ns}.data run data get storage {ns}:gun all.stats.{COOLDOWN}
execute if data storage {ns}:gun all.stats.{FIRE_MODES}[0].cooldown store result score #cooldown {ns}.data run data get storage {ns}:gun all.stats.{FIRE_MODES}[0].cooldown
execute if data storage {ns}:gun all.stats.pap_level if data storage {ns}:gun all.stats.{FIRE_MODES}[0].pap_cooldown store result score #cooldown {ns}.data run data get storage {ns}:gun all.stats.{FIRE_MODES}[0].pap_cooldown
execute if score #fire_mode_is_burst {ns}.data matches 1 run function {ns}:v{version}/player/burst_cooldown

# Timeslip (zombies): halves the throw cooldown of grenades and equipment.
execute if score @s {ns}.special.timeslip matches 1 if data storage {ns}:gun all.stats.{GRENADE_TYPE} run scoreboard players operation #cooldown {ns}.data /= #2 {ns}.data

# As an expiry tick: now + cooldown.
scoreboard players operation #cooldown {ns}.data += #total_tick {ns}.data
scoreboard players operation @s {ns}.cooldown = #cooldown {ns}.data

function {ns}:v{version}/player/fire_weapon

# Weapon data in mgs:signals.
data modify storage {ns}:signals on_shoot set value {{}}
data modify storage {ns}:signals on_shoot.weapon set from storage {ns}:gun all
function #{ns}:signals/on_shoot
""")

	# Grenade, projectile or hitscan.
	write_versioned_function("player/fire_weapon", f"""
execute if data storage {ns}:gun all.stats.{PELLET_COUNT} store result score #bullets_to_fire {ns}.data run data get storage {ns}:gun all.stats.{PELLET_COUNT}

# Only the first 3 entities hit by a shot (all pellets) bleed, against lag when piercing a horde.
scoreboard players set #hit_particles_left {ns}.data 3

execute if data storage {ns}:gun all.stats.{GRENADE_TYPE} run return run function {ns}:v{version}/grenade/throw

# Weapons with projectile config fire slow projectiles instead of a raycast.
execute if data storage {ns}:gun all.stats.{PROJECTILE_SPEED} run return run function {ns}:v{version}/projectile/summon_loop

function {ns}:v{version}/player/shoot
""")

	# #cooldown holds the weapon's cooldown on entry and leaves with this round's.
	write_versioned_function("player/burst_cooldown", f"""
execute if data storage {ns}:gun all.stats.{FIRE_MODES}[0].burst_spacing store result score #cooldown {ns}.data run data get storage {ns}:gun all.stats.{FIRE_MODES}[0].burst_spacing

# First round: pending_clicks = (burst - 1) x spacing sustains the burst without the button held.
execute if score @s {ns}.burst_count matches 0 run scoreboard players operation @s {ns}.pending_clicks = #burst_limit {ns}.data
execute if score @s {ns}.burst_count matches 0 run scoreboard players remove @s {ns}.pending_clicks 1
execute if score @s {ns}.burst_count matches 0 run scoreboard players operation @s {ns}.pending_clicks *= #cooldown {ns}.data

scoreboard players add @s {ns}.burst_count 1

# Last round: the pause before the next burst.
scoreboard players set #burst_pause {ns}.data 0
execute if score @s {ns}.burst_count >= #burst_limit {ns}.data store result score #burst_pause {ns}.data run data get storage {ns}:gun all.stats.{FIRE_MODES}[0].burst_pause
scoreboard players operation #cooldown {ns}.data += #burst_pause {ns}.data
""")

	write_versioned_function("player/shoot", f"""
# Accuracy depends on the movement.
function {ns}:v{version}/raycast/accuracy/get_value

# Deadshot Daiquiri (zombies): spread to 65%.
execute if score @s {ns}.special.deadshot matches 1 run function {ns}:v{version}/raycast/accuracy/deadshot_scale

# Raycast, and a cloud particle forward.
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^2 run particle minecraft:cloud ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[tag=!bs.raycast.omit,distance=..32]
execute anchored eyes positioned ^ ^ ^ summon marker run function {ns}:v{version}/raycast/main
tag @s remove bs.raycast.omit

scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/player/shoot
""")

	write_versioned_function("raycast/main", f"""
# A copy, so pellets do not modify the original.
data modify storage {ns}:temp damage set from storage {ns}:gun all.stats.{DAMAGE}

tp @s ~ ~ ~ ~ ~
function {ns}:v{version}/raycast/accuracy/apply_spread

# Each sound type plays once per shot.
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

# https://docs.mcbookshelf.dev/en/latest/modules/raycast.html#run-the-raycast
execute at @s run function #bs.raycast:run with storage {ns}:input

kill @s
""")

