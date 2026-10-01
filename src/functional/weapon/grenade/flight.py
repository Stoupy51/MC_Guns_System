""" Grenade flight: movement, bouncing, the semtex stick and following a stuck target. """
# Imports
from stewbeet import Conventions, Mem, write_versioned_function

from ....config.stats.keys import GRENADE_TYPE, PROJECTILE_GRAVITY


# Functions
def write_grenade_flight() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("grenade/tick", f"""
# Stuck (semtex on a surface) or in its smoke or flash phase.
execute if entity @s[tag={ns}.grenade_stuck] run return run function {ns}:v{version}/grenade/tick_stuck
execute if entity @s[tag={ns}.grenade_active_effect] run return run function {ns}:v{version}/grenade/tick_effect

# Tumble in proportion to speed, so it stops spinning as it comes to rest.
# #gr_speed = |vx| + |vy| + |vz|, in thousandths of a block per tick.
scoreboard players operation #gr_speed {ns}.data = @s bs.vel.x
execute if score #gr_speed {ns}.data matches ..-1 run scoreboard players operation #gr_speed {ns}.data *= #minus_one {ns}.data
scoreboard players operation #gr_sv {ns}.data = @s bs.vel.y
execute if score #gr_sv {ns}.data matches ..-1 run scoreboard players operation #gr_sv {ns}.data *= #minus_one {ns}.data
scoreboard players operation #gr_speed {ns}.data += #gr_sv {ns}.data
scoreboard players operation #gr_sv {ns}.data = @s bs.vel.z
execute if score #gr_sv {ns}.data matches ..-1 run scoreboard players operation #gr_sv {ns}.data *= #minus_one {ns}.data
scoreboard players operation #gr_speed {ns}.data += #gr_sv {ns}.data

# About 0.44 rad per block/tick of speed, in 1e-4 rad units; no update at rest.
scoreboard players operation #gr_speed {ns}.data *= #44 {ns}.data
scoreboard players operation #gr_speed {ns}.data /= #10 {ns}.data
execute if score #gr_speed {ns}.data matches 1.. run function {ns}:v{version}/grenade/spin_tick

execute store result score #proj_gravity {ns}.data run data get entity @s data.config.{PROJECTILE_GRAVITY}
scoreboard players operation @s bs.vel.y -= #proj_gravity {ns}.data

# Bookshelf move with collision: damped_bounce (frag, smoke, flash) or stick (semtex, web).
execute if data entity @s data.config{{{GRENADE_TYPE}:"semtex"}} run return run function {ns}:v{version}/grenade/move_semtex
execute if data entity @s data.config{{{GRENADE_TYPE}:"web"}} run return run function {ns}:v{version}/grenade/move_semtex
function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:false,ignored_blocks:"#{ns}:v{version}/projectile_pass_through",on_collision:"function {ns}:v{version}/grenade/on_bounce"}}}}

# white_smoke, which the shader marker detection does not mistake for a marker.
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

# Attraction (taunt and aggro pulses); does nothing outside zombies.
execute if entity @s[tag={ns}.monkey_bomb] at @s run function {ns}:v{version}/zombies/monkey/tick

scoreboard players operation @s {ns}.data -= #tick_delta {ns}.data

execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/detonate
""")

	## Semtex sticks instead of bouncing.
	write_versioned_function("grenade/move_semtex", f"""
execute store result score #proj_gravity {ns}.data run data get entity @s data.config.{PROJECTILE_GRAVITY}
scoreboard players operation @s bs.vel.y -= #proj_gravity {ns}.data

# Sticks to the first surface or entity; during the launch grace period entities are skipped, so it never sticks to the thrower.
scoreboard players remove @s {ns}.grenade_launch 1
execute if score @s {ns}.grenade_launch matches 0.. run function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:false,ignored_blocks:"#{ns}:v{version}/projectile_pass_through",on_collision:"function {ns}:v{version}/grenade/on_stick"}}}}
execute unless score @s {ns}.grenade_launch matches 0.. run function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:true,ignored_blocks:"#{ns}:v{version}/projectile_pass_through",on_collision:"function {ns}:v{version}/grenade/on_stick"}}}}

# white_smoke, which the shader marker detection does not mistake for a marker.
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

scoreboard players operation @s {ns}.data -= #tick_delta {ns}.data

execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/detonate
""")

	## Frag, smoke and flash.
	write_versioned_function("grenade/on_bounce",
"""
function #bs.move:callback/damped_bounce

playsound minecraft:entity.item.pickup player @a[distance=..32] ~ ~ ~ 0.5 0.5
""")

	## Semtex.
	write_versioned_function("grenade/on_stick", f"""
function #bs.move:callback/stick

# The tick skips movement.
tag @s add {ns}.grenade_stuck

# hit_flag -1 is an entity: pair the grenade with it.
execute if score $move.hit_flag bs.lambda matches -1 run function {ns}:v{version}/grenade/stick_to_entity

# A web grenade bursts at once on a mob hit, but waits its fuse on a surface.
execute if score $move.hit_flag bs.lambda matches -1 if data entity @s data.config{{{GRENADE_TYPE}:"web"}} run return run function {ns}:v{version}/grenade/detonate

playsound minecraft:block.honey_block.place player @a[distance=..32] ~ ~ ~ 1 1.2
""")

	## Pairs grenade and entity through a unique score id.
	write_versioned_function("grenade/stick_to_entity", f"""
scoreboard players add #semtex_id {ns}.data 1

scoreboard players operation @s {ns}.stuck_id = #semtex_id {ns}.data
execute positioned ~ ~-1 ~ run scoreboard players operation @n[type=!#{ns}:ignore,distance=..2,tag=!{ns}.grenade,tag=!{ns}.slow_bullet,{Conventions.GLOBAL_KILL.avoid},nbt=!{{Invulnerable:true}}] {ns}.stuck_id = #semtex_id {ns}.data

tag @s add {ns}.stuck_to_entity
""")

	write_versioned_function("grenade/tick_stuck", f"""
execute if entity @s[tag={ns}.stuck_to_entity] run function {ns}:v{version}/grenade/follow_entity

scoreboard players operation @s {ns}.data -= #tick_delta {ns}.data

# Blinking before the blast.
particle small_flame ~ ~0.3 ~ 0 0 0 0 1 force @a[distance=..32]

execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/detonate
""")

	write_versioned_function("grenade/follow_entity", f"""
tag @s add {ns}.tp_me

scoreboard players operation #my_stuck {ns}.data = @s {ns}.stuck_id

# The entity with the same stuck_id that is not a grenade.
execute as @e[scores={{{ns}.stuck_id=1..}}] if score @s {ns}.stuck_id = #my_stuck {ns}.data unless entity @s[tag={ns}.grenade] at @s run tp @n[tag={ns}.tp_me] ~ ~ ~

tag @s remove {ns}.tp_me
""")

