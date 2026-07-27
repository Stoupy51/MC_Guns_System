""" Summoning one projectile per pellet, and the entity's initial state and model. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import BASE_WEAPON, DAMAGE, EXPLOSION_DAMAGE, EXPLOSION_DECAY, EXPLOSION_RADIUS, PROJECTILE_GRAVITY, PROJECTILE_LIFETIME, PROJECTILE_MODEL, PROJECTILE_SPEED


# Functions
def write_projectile_summon() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Summon loop (supports pellet_count for multiple projectiles)
	write_versioned_function("projectile/summon_loop", f"""
# Summon a projectile
function {ns}:v{version}/projectile/summon

# Loop for remaining pellets
scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/projectile/summon_loop
""")

	## Summon projectile Called from projectile/summon_loop
	proj_stats = [EXPLOSION_DAMAGE, EXPLOSION_DECAY, EXPLOSION_RADIUS, DAMAGE, PROJECTILE_GRAVITY, PROJECTILE_SPEED, PROJECTILE_LIFETIME, PROJECTILE_MODEL, BASE_WEAPON, "pap_level"]
	proj_copy = "\n".join(f"data modify storage {ns}:temp proj.{s} set from storage {ns}:gun all.stats.{s}" for s in proj_stats)
	write_versioned_function("projectile/summon", f"""
# Get accuracy value and apply spread
function {ns}:v{version}/raycast/accuracy/get_value

# Prepare projectile data in storage before summoning
data modify storage {ns}:temp proj set value {{}}
{proj_copy}

# Summon the projectile entity at the player's eye position
execute anchored eyes positioned ^ ^ ^0.69 summon item_display run function {ns}:v{version}/projectile/init

# Increment slow bullet counter
scoreboard players add #slow_bullet_count {ns}.data 1
""")

	## Initialize the newly summoned projectile marker
	write_versioned_function("projectile/init", f"""
# Tag as slow bullet
tag @s add {ns}.slow_bullet

# Store shooter UUID for damage attribution
data modify entity @s data.shooter set from entity @n[tag={ns}.ticking] UUID

# Copy explosion and projectile config from temp storage
data modify entity @s data.config set from storage {ns}:temp proj

# Set the visual model on the item_display entity (ray_gun is invisible - no projectile model)
execute store success score #is_ray_gun {ns}.data if data entity @s data.config{{{BASE_WEAPON}:"ray_gun"}}
execute if score #is_ray_gun {ns}.data matches 0 run function {ns}:v{version}/projectile/set_model with entity @s data.config

# Set lifetime score
execute store result score @s {ns}.data run data get storage {ns}:temp proj.{PROJECTILE_LIFETIME}

# Calculate velocity from the player's look direction and teleport back
function {ns}:v{version}/shared/calc_velocity
""")

	## Set visual model on the item_display (macro function)
	write_versioned_function("projectile/set_model", f"""
$data modify entity @s item set value {{id:"minecraft:paper", count:1, components:{{"minecraft:item_model":"{ns}:$({PROJECTILE_MODEL})"}}}}
data modify entity @s item_display set value "fixed"
data modify entity @s brightness set value {{sky: 15, block: 15}}
""")

