""" Projectile flight: gravity, movement and what happens when it hits something. """
# Imports
from stewbeet import Conventions, Mem, write_versioned_function

from .....config.stats.keys import BASE_WEAPON, PROJECTILE_GRAVITY


# Functions
def write_projectile_flight() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("projectile/tick", f"""
execute store result score #proj_gravity {ns}.data run data get entity @s data.config.{PROJECTILE_GRAVITY}
scoreboard players operation @s bs.vel.y -= #proj_gravity {ns}.data

# Bookshelf move with collision; custom ignored_blocks, so barriers never stop projectiles.
function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:true,ignored_blocks:"#{ns}:v{version}/projectile_pass_through",on_collision:"function {ns}:v{version}/projectile/on_collision"}}}}

execute at @s run function {ns}:v{version}/projectile/post_vel
""")
	write_versioned_function("projectile/post_vel", f"""
# Collision: explode and stop.
execute if entity @s[tag={ns}.exploding] run return run function {ns}:v{version}/projectile/explode

# Ray Gun: green swirl, Pack-a-Punched: red; others flame and smoke.
scoreboard players set #ray_gun {ns}.data 0
execute if data entity @s data.config{{{BASE_WEAPON}:"ray_gun"}} run scoreboard players set #ray_gun {ns}.data 1
execute if score #ray_gun {ns}.data matches 1 if data entity @s data.config.pap_level run scoreboard players set #ray_gun {ns}.data 2
execute if score #ray_gun {ns}.data matches 2 run particle dust{{color:[0.8,0.0,0.0],scale:1.5}} ~ ~ ~ 0.1 0.1 0.1 0 8 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 2 run particle crimson_spore ~ ~ ~ 0.1 0.1 0.1 0 3 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 1 run particle dust{{color:[0.0,0.8,0.0],scale:1.5}} ~ ~ ~ 0.1 0.1 0.1 0 8 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 1 run particle glow ~ ~ ~ 0.1 0.1 0.1 0 3 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle flame ~ ~ ~ 0.05 0.05 0.05 0.02 3 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle smoke ~ ~ ~ 0.1 0.1 0.1 0.01 2 force @a[distance=..128]

scoreboard players remove @s {ns}.data 1

# Lifetime over: explode.
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/projectile/explode
""")

	## Called by bs.move:apply_vel on a block or entity hit.
	write_versioned_function("projectile/on_collision", f"""
# The nearest non-immune entity takes the direct-hit damage in explode; 2.5 blocks covers feet to head at any height up to 2.5.
tag @e[tag={ns}.direct_hit] remove {ns}.direct_hit
execute as @n[distance=..2.5,type=!#{ns}:ignore,tag=!{ns}.slow_bullet,{Conventions.GLOBAL_KILL.avoid},nbt=!{{Invulnerable:true}}] run tag @s add {ns}.direct_hit

tag @s add {ns}.exploding

scoreboard players set $move.vel.x bs.lambda 0
scoreboard players set $move.vel.y bs.lambda 0
scoreboard players set $move.vel.z bs.lambda 0
""")

