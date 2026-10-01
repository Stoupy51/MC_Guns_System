""" Lingering effects, entity cleanup and the movement tick hook. """
# Imports
from stewbeet import Mem, write_tick_file, write_versioned_function

from ....config.stats.keys import GRENADE_EFFECT_RADIUS


# Functions
def write_grenade_effects() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("grenade/tick_effect", f"""
scoreboard players operation @s {ns}.data -= #tick_delta {ns}.data

execute store result score #effect_r {ns}.data run data get entity @s data.config.{GRENADE_EFFECT_RADIUS}
function {ns}:v{version}/grenade/smoke_particles

# Every 20 ticks.
execute store result score #smoke_tick {ns}.data run scoreboard players get @s {ns}.data
scoreboard players operation #smoke_tick {ns}.data %= #20 {ns}.data
execute if score #smoke_tick {ns}.data matches 0 run playsound minecraft:block.fire.extinguish player @a[distance=..32] ~ ~ ~ 0.3 0.5

execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/delete
""")

	write_versioned_function("grenade/smoke_particles",
"""
# Within the effect radius.
particle campfire_signal_smoke ~ ~0.5 ~ 2 1.5 2 0.01 50 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~1 ~ 1.5 1 1.5 0.02 20 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~0.3 ~ 2 0.5 2 0.005 10 force @a[distance=..128]
""")

	write_versioned_function("grenade/delete", f"""
execute if entity @s[tag={ns}.stuck_to_entity] run function {ns}:v{version}/grenade/cleanup_stuck_entity

kill @s
""")

	write_versioned_function("grenade/cleanup_stuck_entity", f"""
scoreboard players operation #my_stuck {ns}.data = @s {ns}.stuck_id

execute as @e[scores={{{ns}.stuck_id=1..}}] if score @s {ns}.stuck_id = #my_stuck {ns}.data unless entity @s[tag={ns}.grenade] run scoreboard players reset @s {ns}.stuck_id
""")

	write_tick_file(f"""
# Not gated on a counter: a desync (a grenade removed outside grenade/delete, a double detonation) could stop every grenade ticking.
# Selecting by tag each tick is cheap and self-correcting.
execute as @e[type=minecraft:item_display,tag={ns}.grenade] at @s run function {ns}:v{version}/grenade/tick
""")

