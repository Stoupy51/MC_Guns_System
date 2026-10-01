""" Summoning one projectile per pellet, and the entity's initial state and model. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import (
	BASE_WEAPON,
	DAMAGE,
	EXPLOSION_DAMAGE,
	EXPLOSION_DECAY,
	EXPLOSION_RADIUS,
	PROJECTILE_GRAVITY,
	PROJECTILE_LIFETIME,
	PROJECTILE_MODEL,
	PROJECTILE_SPEED,
)


# Functions
def write_projectile_summon() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## pellet_count gives several projectiles.
	write_versioned_function("projectile/summon_loop", f"""
function {ns}:v{version}/projectile/summon

scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/projectile/summon_loop
""")

	proj_stats = [EXPLOSION_DAMAGE, EXPLOSION_DECAY, EXPLOSION_RADIUS, DAMAGE, PROJECTILE_GRAVITY, PROJECTILE_SPEED, PROJECTILE_LIFETIME, PROJECTILE_MODEL, BASE_WEAPON, "pap_level"]
	proj_copy = "\n".join(f"data modify storage {ns}:temp proj.{s} set from storage {ns}:gun all.stats.{s}" for s in proj_stats)
	write_versioned_function("projectile/summon", f"""
# Spread from the accuracy value.
function {ns}:v{version}/raycast/accuracy/get_value

data modify storage {ns}:temp proj set value {{}}
{proj_copy}

# At the muzzle, 0.69 ahead of the eyes, only when that spot is open, else at the eyes: flush against a wall the muzzle is inside it,
# and a projectile starting inside a block never registers an entry collision (bs.move sees it leave), so it went through thick walls.
execute anchored eyes positioned ^ ^ ^0.69 store success score #proj_muzzle_free {ns}.data if block ~ ~ ~ #{ns}:v{version}/projectile_pass_through
execute if score #proj_muzzle_free {ns}.data matches 1 anchored eyes positioned ^ ^ ^0.69 summon item_display run function {ns}:v{version}/projectile/init
execute if score #proj_muzzle_free {ns}.data matches 0 anchored eyes positioned ^ ^ ^0 summon item_display run function {ns}:v{version}/projectile/init

scoreboard players add #slow_bullet_count {ns}.data 1
""")

	write_versioned_function("projectile/init", f"""
tag @s add {ns}.slow_bullet

# For damage attribution.
data modify entity @s data.shooter set from entity @n[tag={ns}.ticking] UUID

data modify entity @s data.config set from storage {ns}:temp proj

# The Ray Gun has no projectile model.
execute store success score #is_ray_gun {ns}.data if data entity @s data.config{{{BASE_WEAPON}:"ray_gun"}}
execute if score #is_ray_gun {ns}.data matches 0 run function {ns}:v{version}/projectile/set_model with entity @s data.config

execute store result score @s {ns}.data run data get storage {ns}:temp proj.{PROJECTILE_LIFETIME}

# From the look direction, then back.
function {ns}:v{version}/shared/calc_velocity
""")

	write_versioned_function("projectile/set_model", f"""
$data modify entity @s item set value {{id:"minecraft:paper", count:1, components:{{"minecraft:item_model":"{ns}:$({PROJECTILE_MODEL})"}}}}
data modify entity @s item_display set value "fixed"
data modify entity @s brightness set value {{sky: 15, block: 15}}
""")

