""" Lingering effects, entity cleanup and the movement tick hook. """
# Imports
from stewbeet import Mem, write_tick_file, write_versioned_function

from ....config.stats.keys import GRENADE_EFFECT_RADIUS


# Functions
def write_grenade_effects() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Tick for active effect grenades (smoke particles)
	write_versioned_function("grenade/tick_effect", f"""
# Decrement effect duration (real-time via #tick_delta)
scoreboard players operation @s {ns}.data -= #tick_delta {ns}.data

# Emit smoke cloud particles
execute store result score #effect_r {ns}.data run data get entity @s data.config.{GRENADE_EFFECT_RADIUS}
function {ns}:v{version}/grenade/smoke_particles

# Play ambient sound occasionally (every 20 ticks)
execute store result score #smoke_tick {ns}.data run scoreboard players get @s {ns}.data
scoreboard players operation #smoke_tick {ns}.data %= #20 {ns}.data
execute if score #smoke_tick {ns}.data matches 0 run playsound minecraft:block.fire.extinguish player @a[distance=..32] ~ ~ ~ 0.3 0.5

# If duration expired, delete
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/delete
""")

	## Smoke particle emission
	write_versioned_function("grenade/smoke_particles",
"""
# Dense smoke cloud within effect radius
particle campfire_signal_smoke ~ ~0.5 ~ 2 1.5 2 0.01 50 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~1 ~ 1.5 1 1.5 0.02 20 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~0.3 ~ 2 0.5 2 0.005 10 force @a[distance=..128]
""")

	## Delete grenade entity
	write_versioned_function("grenade/delete", f"""
# If stuck to an entity, clean up the target's stuck_id
execute if entity @s[tag={ns}.stuck_to_entity] run function {ns}:v{version}/grenade/cleanup_stuck_entity

# Remove the grenade entity
kill @s
""")

	## Clean up stuck_id from the paired entity
	write_versioned_function("grenade/cleanup_stuck_entity", f"""
# Read my stuck ID
scoreboard players operation #my_stuck {ns}.data = @s {ns}.stuck_id

# Find the paired entity and reset its stuck_id
execute as @e[scores={{{ns}.stuck_id=1..}}] if score @s {ns}.stuck_id = #my_stuck {ns}.data unless entity @s[tag={ns}.grenade] run scoreboard players reset @s {ns}.stuck_id
""")

	## Tick file entry for grenade movement
	write_tick_file(f"""
# Tick every live grenade. This is intentionally NOT gated on a running count: a counter desync
# (e.g. a grenade removed outside grenade/delete, or a double-detonate) used to drop the count to 0
# and freeze EVERY projectile's ticking ("no more items to tick", monkey bombs included). Selecting
# by tag each tick is cheap and self-correcting.
execute as @e[tag={ns}.grenade] at @s run function {ns}:v{version}/grenade/tick
""")

