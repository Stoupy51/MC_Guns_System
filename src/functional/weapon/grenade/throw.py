""" Throwing a grenade: summoning the entity, its model and the tumble animation. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import (
	EXPLOSION_DAMAGE,
	EXPLOSION_DECAY,
	EXPLOSION_RADIUS,
	GRENADE_DURATION,
	GRENADE_EFFECT_RADIUS,
	GRENADE_FUSE,
	GRENADE_TYPE,
	PROJECTILE_GRAVITY,
	PROJECTILE_MODEL,
	PROJECTILE_SPEED,
	REMAINING_BULLETS,
)


# Functions
def write_grenade_throw() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Throw grenade (called from fire_weapon when grenade_type is present)
	grenade_stats = [GRENADE_TYPE, GRENADE_FUSE, GRENADE_DURATION, GRENADE_EFFECT_RADIUS, EXPLOSION_DAMAGE, EXPLOSION_DECAY, EXPLOSION_RADIUS, PROJECTILE_GRAVITY, PROJECTILE_SPEED, PROJECTILE_MODEL]
	grenade_copy = "\n".join(f"data modify storage {ns}:temp grenade.{s} set from storage {ns}:gun all.stats.{s}" for s in grenade_stats)
	write_versioned_function("grenade/throw", f"""
# Prepare grenade data in storage before summoning
data modify storage {ns}:temp grenade set value {{}}
{grenade_copy}

# Keep camo variants: use the held item's actual model when thrown by a player
# (mobs have no SelectedItem in storage and fall back to the base {PROJECTILE_MODEL} stat)
execute if entity @s[type=player] if data storage {ns}:gun SelectedItem.components."minecraft:item_model" run data modify storage {ns}:temp grenade.model_override set from storage {ns}:gun SelectedItem.components."minecraft:item_model"

# Summon loop (supports pellet_count for multiple grenades)
function {ns}:v{version}/grenade/summon_loop

# Consume one grenade from the stack (decrease count by 1) - skip if infinite ammo
execute unless score @s {ns}.special.infinite_ammo matches 1.. run item modify entity @p[tag={ns}.ticking] weapon.mainhand {ns}:v{version}/grenade/consume_one

# Set remaining_bullets to 2 so ammo/decrease (which runs after) reduces it to 1 for the next throw
scoreboard players set @s {ns}.{REMAINING_BULLETS} 2
""")  # noqa: E501

	## Summon loop (supports pellet_count for multiple grenades)
	write_versioned_function("grenade/summon_loop", f"""
# Summon a grenade
function {ns}:v{version}/grenade/summon

# Loop for remaining grenades
scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/grenade/summon_loop
""")

	## Summon a single grenade entity
	write_versioned_function("grenade/summon", f"""
# Get accuracy value and apply spread
function {ns}:v{version}/raycast/accuracy/get_value

# Summon the grenade entity at the player's eye position
execute anchored eyes positioned ^ ^ ^0.5 summon item_display run function {ns}:v{version}/grenade/init
""")

	## Initialize the newly summoned grenade entity
	write_versioned_function("grenade/init", f"""
# Tag as grenade
tag @s add {ns}.grenade

# Store shooter UUID for damage attribution
data modify entity @s data.shooter set from entity @n[tag={ns}.ticking] UUID

# Copy grenade config from temp storage
data modify entity @s data.config set from storage {ns}:temp grenade

# Set the visual model on the item_display entity (camo variants override the base model)
function {ns}:v{version}/grenade/set_model with entity @s data.config
execute if data entity @s data.config.model_override run function {ns}:v{version}/grenade/set_model_override with entity @s data.config

# Set fuse timer from config
execute store result score @s {ns}.data run data get entity @s data.config.{GRENADE_FUSE}

# Monkey bomb: tag + summon its zombie-attraction taunt (zombies module owns the behavior)
execute if data entity @s data.config{{{GRENADE_TYPE}:"monkey_bomb"}} run function {ns}:v{version}/zombies/monkey/on_throw

# Launch grace period: disable entity collision for 3 ticks to avoid sticking to the thrower
scoreboard players set @s {ns}.grenade_launch 3

# Calculate velocity from the player's look direction and teleport back
function {ns}:v{version}/shared/calc_velocity
""")

	## Set visual model on the item_display (macro function)
	write_versioned_function("grenade/set_model", f"""
$data modify entity @s item set value {{id:"minecraft:paper", count:1, components:{{"minecraft:item_model":"{ns}:$({PROJECTILE_MODEL})"}}}}
data modify entity @s item_display set value "fixed"
data modify entity @s brightness set value {{sky: 15, block: 15}}
data modify entity @s teleport_duration set value 1
""")

	## Override the model with the thrower's actual held item model (keeps camo variants)
	write_versioned_function("grenade/set_model_override", """
$data modify entity @s item.components."minecraft:item_model" set value "$(model_override)"
""")

	## Tumble animation: accumulate the per-grenade spin angle and apply it with 1-tick interpolation (angle wraps at 2π = 62832 units; quaternion slerp keeps the wrap-around seamless)
	write_versioned_function("grenade/spin_tick", f"""
scoreboard players add @s {ns}.grenade_spin 0
scoreboard players operation @s {ns}.grenade_spin += #gr_speed {ns}.data
scoreboard players operation @s {ns}.grenade_spin %= #62832 {ns}.data
execute store result storage {ns}:temp _gr_spin.angle float 0.0001 run scoreboard players get @s {ns}.grenade_spin
function {ns}:v{version}/grenade/apply_spin with storage {ns}:temp _gr_spin
""")

	write_versioned_function("grenade/apply_spin", """
$data modify entity @s transformation.left_rotation set value {axis:[1f,0f,0f],angle:$(angle)}
data merge entity @s {start_interpolation:0,interpolation_duration:1}
""")

