""" The turret trap: target selection, line of sight, aiming and its bullet. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_turret() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Turret trap: pick the nearest *visible* zombie in the effect box, aim the head at it, then fire a bullet
	write_versioned_function("zombies/traps/turret_fire", f"""
# @s = trap center marker, at @s position
# Remember this trap's id so we can find/rotate the matching head display and use it as the muzzle
scoreboard players operation #turret_tid {ns}.data = @s {ns}.zb.trap.id

# Tag every zombie inside the effect box as a candidate, keep only those the head has line of sight to,
# then pick the one nearest the turret center
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag={ns}.zombie_round,tag=!{ns}.zb_rising,dx=$(sx),dy=$(sy),dz=$(sz)] run tag @s add {ns}._turret_cand
execute as @e[tag={ns}._turret_cand] run function {ns}:v{version}/zombies/traps/turret_check_los
# Capture, via the tag command's success, whether a target was selected — avoids the global
# `unless entity @e[tag={ns}._turret_target]` scan below. limit=1 means this runs at most once;
# #turret_has_target stays 0 if there was no visible zombie (the body never executes).
scoreboard players set #turret_has_target {ns}.data 0
execute as @e[tag={ns}._turret_visible,sort=nearest,limit=1] store success score #turret_has_target {ns}.data run tag @s add {ns}._turret_target
tag @e[tag={ns}._turret_cand] remove {ns}._turret_cand
tag @e[tag={ns}._turret_visible] remove {ns}._turret_visible

# No visible zombie in range: nothing to aim at or shoot
execute if score #turret_has_target {ns}.data matches 0 run return 0

# Aim this turret's head display at the target (yaw + pitch via facing entity, smoothed by teleport_duration)
execute as @e[tag={ns}.trap_head,predicate={ns}:v{version}/zombies/traps/turret_id_match] at @s run tp @s ~ ~ ~ facing entity @n[tag={ns}._turret_target] eyes

# Fire the bullet straight from the head display itself (no manual offset) toward the target
execute as @e[tag={ns}.trap_head,predicate={ns}:v{version}/zombies/traps/turret_id_match] at @s facing entity @n[tag={ns}._turret_target] eyes positioned ^ ^ ^1 run function {ns}:v{version}/zombies/traps/turret_shoot

# Clear the temporary target tag
tag @e[tag={ns}._turret_target] remove {ns}._turret_target
""")

	## Line-of-sight gate: tag the candidate zombie as visible only if the turret can see it. can_see_ata raycasts from the execution position to @s (the zombie), returning 1 if unobstructed.
	## The turret head sits half inside a barricade block, so casting from there would self-block; instead we cast from 1.5 blocks below the interaction entity (clear of the barricade) - matched by id via predicate.
	write_versioned_function("zombies/traps/turret_check_los", f"""
# @s = candidate zombie
scoreboard players set #turret_vis {ns}.data 0
execute at @e[tag={ns}.trap_interact,predicate={ns}:v{version}/zombies/traps/turret_id_match] positioned ~ ~-1.5 ~ store result score #turret_vis {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #turret_vis {ns}.data matches 1 run tag @s add {ns}._turret_visible
""")

	## Fire the turret bullet: raycast that stops at the first entity hit
	write_versioned_function("zombies/traps/turret_shoot", f"""
# @s = trap center marker (execution position = turret muzzle, facing the target)
# Tracer particle + G3A3 gunshot (close report + 'large' acoustics crack, same as a player firing a G3A3)
particle minecraft:crit ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[distance=..64]
function {ns}:v{version}/sound/turret_fire

# Raycast with piercing 0: the ray stops at the first entity hit,
# so a player standing between the turret and the zombies takes the bullet instead
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage {ns}:input with.entities set value "!global.ignore"
data modify storage {ns}:input with.piercing set value 0
data modify storage {ns}:input with.max_distance set value 32
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/empty"
data modify storage {ns}:input with.ignored_entities set value "#{ns}:ignore"
data modify storage {ns}:input with.on_targeted_entity set value "function {ns}:v{version}/zombies/traps/turret_hit"
function #bs.raycast:run with storage {ns}:input
""")

	## Turret bullet impact (@s = hit entity, positioned at the hit point)
	write_versioned_function("zombies/traps/turret_hit", f"""
# Impact particles
particle minecraft:crit ~ ~1 ~ 0.2 0.3 0.2 0.1 8 force @a[distance=..48]

# Zombie hit: 45% of its max health
execute if entity @s[tag={ns}.zombie_round] store result storage {ns}:temp _trap_dmg.amount int 1 run attribute @s minecraft:max_health get 0.45
execute if entity @s[tag={ns}.zombie_round] run data modify storage {ns}:temp _trap_dmg.type set value "{ns}:bullet"
execute if entity @s[tag={ns}.zombie_round] run return run function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _trap_dmg

# Player caught between the turret and the zombies: 2 damage
execute if entity @s[type=player,gamemode=!creative,gamemode=!spectator] if score @s {ns}.zb.in_game matches 1.. run damage @s 2 {ns}:bullet
""")

