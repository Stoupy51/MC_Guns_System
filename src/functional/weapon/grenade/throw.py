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

	## Run from fire_weapon when grenade_type is set.
	grenade_stats = [GRENADE_TYPE, GRENADE_FUSE, GRENADE_DURATION, GRENADE_EFFECT_RADIUS, EXPLOSION_DAMAGE, EXPLOSION_DECAY, EXPLOSION_RADIUS, PROJECTILE_GRAVITY, PROJECTILE_SPEED, PROJECTILE_MODEL]
	grenade_copy = "\n".join(f"data modify storage {ns}:temp grenade.{s} set from storage {ns}:gun all.stats.{s}" for s in grenade_stats)
	write_versioned_function("grenade/throw", f"""
data modify storage {ns}:temp grenade set value {{}}
{grenade_copy}

# Player throws keep the held item's model (camo variants); mobs have no SelectedItem and use the base {PROJECTILE_MODEL}.
execute if entity @s[type=player] if data storage {ns}:gun SelectedItem.components."minecraft:item_model" run data modify storage {ns}:temp grenade.model_override set from storage {ns}:gun SelectedItem.components."minecraft:item_model"

# pellet_count gives several grenades.
function {ns}:v{version}/grenade/summon_loop

# Unless infinite ammo.
execute unless score @s {ns}.special.infinite_ammo matches 1.. run item modify entity @p[tag={ns}.ticking] weapon.mainhand {ns}:v{version}/grenade/consume_one

# ammo/decrease runs next and brings it to 1.
scoreboard players set @s {ns}.{REMAINING_BULLETS} 2
""")

	write_versioned_function("grenade/summon_loop", f"""
function {ns}:v{version}/grenade/summon

scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/grenade/summon_loop
""")

	write_versioned_function("grenade/summon", f"""
# Spread from the accuracy value.
function {ns}:v{version}/raycast/accuracy/get_value

execute anchored eyes positioned ^ ^ ^0.5 summon item_display run function {ns}:v{version}/grenade/init
""")

	write_versioned_function("grenade/init", f"""
tag @s add {ns}.grenade

# For damage attribution.
data modify entity @s data.shooter set from entity @n[tag={ns}.ticking] UUID

data modify entity @s data.config set from storage {ns}:temp grenade

# Camo variants override the base model.
function {ns}:v{version}/grenade/set_model with entity @s data.config
execute if data entity @s data.config.model_override run function {ns}:v{version}/grenade/set_model_override with entity @s data.config

execute store result score @s {ns}.data run data get entity @s data.config.{GRENADE_FUSE}

# The zombies module owns the attraction.
execute if data entity @s data.config{{{GRENADE_TYPE}:"monkey_bomb"}} run function {ns}:v{version}/zombies/monkey/on_throw

# No entity collision for 3 ticks, so it never sticks to the thrower.
scoreboard players set @s {ns}.grenade_launch 3

# From the look direction, then back.
function {ns}:v{version}/shared/calc_velocity
""")

	write_versioned_function("grenade/set_model", f"""
$data modify entity @s item set value {{id:"minecraft:paper", count:1, components:{{"minecraft:item_model":"{ns}:$({PROJECTILE_MODEL})"}}}}
data modify entity @s item_display set value "fixed"
data modify entity @s brightness set value {{sky: 15, block: 15}}
data modify entity @s teleport_duration set value 1
""")

	## Keeps camo variants.
	write_versioned_function("grenade/set_model_override", """
$data modify entity @s item.components."minecraft:item_model" set value "$(model_override)"
""")

	## Accumulates the spin angle (wraps at 2π = 62832 units) with 1-tick interpolation; quaternion slerp keeps the wrap seamless.
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

