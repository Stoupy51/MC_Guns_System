""" Grenade flight: movement, bouncing, the semtex stick and following a stuck target. """
# Imports
from stewbeet import Conventions, Mem, write_versioned_function

from ....config.stats.keys import GRENADE_TYPE, PROJECTILE_GRAVITY


# Functions
def write_grenade_flight() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Tick function for each grenade entity
	write_versioned_function("grenade/tick", f"""
# Skip if grenade is stuck (semtex on a surface) or in smoke/flash effect phase
execute if entity @s[tag={ns}.grenade_stuck] run return run function {ns}:v{version}/grenade/tick_stuck
execute if entity @s[tag={ns}.grenade_active_effect] run return run function {ns}:v{version}/grenade/tick_effect

# Tumble proportionally to current speed: fast while flying, stops as the grenade comes to rest
# #gr_speed = |vx| + |vy| + |vz| (thousandths of a block per tick)
scoreboard players operation #gr_speed {ns}.data = @s bs.vel.x
execute if score #gr_speed {ns}.data matches ..-1 run scoreboard players operation #gr_speed {ns}.data *= #minus_one {ns}.data
scoreboard players operation #gr_sv {ns}.data = @s bs.vel.y
execute if score #gr_sv {ns}.data matches ..-1 run scoreboard players operation #gr_sv {ns}.data *= #minus_one {ns}.data
scoreboard players operation #gr_speed {ns}.data += #gr_sv {ns}.data
scoreboard players operation #gr_sv {ns}.data = @s bs.vel.z
execute if score #gr_sv {ns}.data matches ..-1 run scoreboard players operation #gr_sv {ns}.data *= #minus_one {ns}.data
scoreboard players operation #gr_speed {ns}.data += #gr_sv {ns}.data

# Angle step ≈ 0.44 rad per (block/tick) of speed, in 1e-4 rad units; skip the update when resting
scoreboard players operation #gr_speed {ns}.data *= #44 {ns}.data
scoreboard players operation #gr_speed {ns}.data /= #10 {ns}.data
execute if score #gr_speed {ns}.data matches 1.. run function {ns}:v{version}/grenade/spin_tick

# Apply gravity (subtract from Y velocity)
execute store result score #proj_gravity {ns}.data run data get entity @s data.config.{PROJECTILE_GRAVITY}
scoreboard players operation @s bs.vel.y -= #proj_gravity {ns}.data

# Move the grenade using Bookshelf's move module with collision detection
# Grenades use damped_bounce by default (frag/smoke/flash) or stick (semtex + web)
execute if data entity @s data.config{{{GRENADE_TYPE}:"semtex"}} run return run function {ns}:v{version}/grenade/move_semtex
execute if data entity @s data.config{{{GRENADE_TYPE}:"web"}} run return run function {ns}:v{version}/grenade/move_semtex
function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:false,ignored_blocks:"#{ns}:v{version}/projectile_pass_through",on_collision:"function {ns}:v{version}/grenade/on_bounce"}}}}

# Trail particle (white_smoke avoids false-positive with shader marker detection)
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

# Monkey bomb: per-tick attraction (taunt follow + periodic aggro pulses; no-op outside zombies)
execute if entity @s[tag={ns}.monkey_bomb] at @s run function {ns}:v{version}/zombies/monkey/tick

# Decrement fuse timer (real-time via #tick_delta)
scoreboard players operation @s {ns}.data -= #tick_delta {ns}.data

# If fuse expired, detonate
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/detonate
""")

	## Move semtex (uses stick collision instead of bounce)
	write_versioned_function("grenade/move_semtex", f"""
# Apply gravity
execute store result score #proj_gravity {ns}.data run data get entity @s data.config.{PROJECTILE_GRAVITY}
scoreboard players operation @s bs.vel.y -= #proj_gravity {ns}.data

# Move with stick callback (semtex sticks to first surface or entity hit)
# During launch grace period, skip entity collision to avoid sticking to the thrower
scoreboard players remove @s {ns}.grenade_launch 1
execute if score @s {ns}.grenade_launch matches 0.. run function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:false,ignored_blocks:"#{ns}:v{version}/projectile_pass_through",on_collision:"function {ns}:v{version}/grenade/on_stick"}}}}
execute unless score @s {ns}.grenade_launch matches 0.. run function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:true,ignored_blocks:"#{ns}:v{version}/projectile_pass_through",on_collision:"function {ns}:v{version}/grenade/on_stick"}}}}

# Trail particle (white_smoke avoids false-positive with shader marker detection)
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

# Decrement fuse timer (real-time via #tick_delta)
scoreboard players operation @s {ns}.data -= #tick_delta {ns}.data

# If fuse expired, detonate
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/detonate
""")  # noqa: E501

	## Bounce collision callback (for frag/smoke/flash grenades)
	write_versioned_function("grenade/on_bounce",
"""
# Apply damped bounce (reduce velocity and reverse direction on collision axis)
function #bs.move:callback/damped_bounce

# Play bounce sound
playsound minecraft:entity.item.pickup player @a[distance=..32] ~ ~ ~ 0.5 0.5
""")

	## Stick collision callback (for semtex)
	write_versioned_function("grenade/on_stick", f"""
# Stop all velocity (stick to the surface)
function #bs.move:callback/stick

# Mark as stuck so tick skips movement
tag @s add {ns}.grenade_stuck

# If we hit an entity (hit_flag = -1 for entities), pair the grenade with the target
execute if score $move.hit_flag bs.lambda matches -1 run function {ns}:v{version}/grenade/stick_to_entity

# Web grenade bursts instantly on a mob hit (hit_flag -1), but sticks to surfaces and waits its fuse
execute if score $move.hit_flag bs.lambda matches -1 if data entity @s data.config{{{GRENADE_TYPE}:"web"}} run return run function {ns}:v{version}/grenade/detonate

# Play stick sound
playsound minecraft:block.honey_block.place player @a[distance=..32] ~ ~ ~ 1 1.2
""")

	## Pair semtex grenade with target entity using unique scoreboard ID
	write_versioned_function("grenade/stick_to_entity", f"""
# Increment the global semtex pairing counter to get a unique ID
scoreboard players add #semtex_id {ns}.data 1

# Assign the same unique ID to both the grenade and the nearest entity
scoreboard players operation @s {ns}.stuck_id = #semtex_id {ns}.data
execute positioned ~ ~-1 ~ run scoreboard players operation @n[type=!#{ns}:ignore,distance=..2,tag=!{ns}.grenade,tag=!{ns}.slow_bullet,{Conventions.GLOBAL_KILL.avoid},nbt=!{{Invulnerable:true}}] {ns}.stuck_id = #semtex_id {ns}.data

# Mark that this grenade is stuck to an entity (not just a block)
tag @s add {ns}.stuck_to_entity
""")  # noqa: E501

	## Tick for stuck grenades (just countdown)
	write_versioned_function("grenade/tick_stuck", f"""
# If stuck to an entity, follow it
execute if entity @s[tag={ns}.stuck_to_entity] run function {ns}:v{version}/grenade/follow_entity

# Decrement fuse timer (real-time via #tick_delta)
scoreboard players operation @s {ns}.data -= #tick_delta {ns}.data

# Blinking particle to indicate it's about to explode
particle small_flame ~ ~0.3 ~ 0 0 0 0 1 force @a[distance=..32]

# If fuse expired, detonate
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/detonate
""")

	## Follow the paired entity (teleport grenade to entity's position)
	write_versioned_function("grenade/follow_entity", f"""
# Tag myself for the teleportation
tag @s add {ns}.tp_me

# Read my stuck ID
scoreboard players operation #my_stuck {ns}.data = @s {ns}.stuck_id

# Find the entity with matching stuck_id (not a grenade) and teleport me to it
execute as @e[scores={{{ns}.stuck_id=1..}}] if score @s {ns}.stuck_id = #my_stuck {ns}.data unless entity @s[tag={ns}.grenade] at @s run tp @n[tag={ns}.tp_me] ~ ~ ~

# Remove temp tag
tag @s remove {ns}.tp_me
""")

