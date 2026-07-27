""" Projectile flight: gravity, movement and what happens when it hits something. """
# Imports
from stewbeet import Conventions, Mem, write_versioned_function

from .....config.stats.keys import BASE_WEAPON, PROJECTILE_GRAVITY


# Functions
def write_projectile_flight() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Tick function for each projectile entity
	write_versioned_function("projectile/tick", f"""
# Apply gravity (subtract from Y velocity)
execute store result score #proj_gravity {ns}.data run data get entity @s data.config.{PROJECTILE_GRAVITY}
scoreboard players operation @s bs.vel.y -= #proj_gravity {ns}.data

# Move the projectile using Bookshelf's move module with collision detection
# (custom ignored_blocks so barrier blocks never stop projectiles)
function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:true,ignored_blocks:"#{ns}:v{version}/projectile_pass_through",on_collision:"function {ns}:v{version}/projectile/on_collision"}}}}

# If collision was detected, explode and stop processing
execute at @s run function {ns}:v{version}/projectile/post_vel
""")
	write_versioned_function("projectile/post_vel", f"""
# If collision was detected, explode and stop processing
execute if entity @s[tag={ns}.exploding] run return run function {ns}:v{version}/projectile/explode

# Trail particles: ray_gun = green dust swirl, upgraded ray_gun = red dust swirl, others = flame + smoke
scoreboard players set #ray_gun {ns}.data 0
execute if data entity @s data.config{{{BASE_WEAPON}:"ray_gun"}} run scoreboard players set #ray_gun {ns}.data 1
execute if score #ray_gun {ns}.data matches 1 if data entity @s data.config.pap_level run scoreboard players set #ray_gun {ns}.data 2
execute if score #ray_gun {ns}.data matches 2 run particle dust{{color:[0.8,0.0,0.0],scale:1.5}} ~ ~ ~ 0.1 0.1 0.1 0 8 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 2 run particle crimson_spore ~ ~ ~ 0.1 0.1 0.1 0 3 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 1 run particle dust{{color:[0.0,0.8,0.0],scale:1.5}} ~ ~ ~ 0.1 0.1 0.1 0 8 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 1 run particle glow ~ ~ ~ 0.1 0.1 0.1 0 3 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle flame ~ ~ ~ 0.05 0.05 0.05 0.02 3 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle smoke ~ ~ ~ 0.1 0.1 0.1 0.01 2 force @a[distance=..128]

# Decrement lifetime
scoreboard players remove @s {ns}.data 1

# If lifetime expired, explode
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/projectile/explode
""")

	## Collision callback (called by bs.move:apply_vel when hitting a block or entity)
	write_versioned_function("projectile/on_collision", f"""
# Tag the nearest non-immune entity as directly hit (for bullet damage in explode)
# distance=..2.5 covers feet-to-head hit at any entity height up to 2.5 blocks
tag @e[tag={ns}.direct_hit] remove {ns}.direct_hit
execute as @n[distance=..2.5,type=!#{ns}:ignore,tag=!{ns}.slow_bullet,{Conventions.GLOBAL_KILL.avoid},nbt=!{{Invulnerable:true}}] run tag @s add {ns}.direct_hit

# Mark for explosion
tag @s add {ns}.exploding

# Stop all remaining velocity to prevent further movement
scoreboard players set $move.vel.x bs.lambda 0
scoreboard players set $move.vel.y bs.lambda 0
scoreboard players set $move.vel.z bs.lambda 0
""")

