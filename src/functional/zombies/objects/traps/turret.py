""" The turret trap: target selection, line of sight, aiming and its bullet. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_turret() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Aim at the nearest visible zombie in the effect box and fire.
	write_versioned_function("zombies/traps/turret_fire", f"""
# Run as the trap centre marker, at it.
scoreboard players operation #turret_tid {ns}.data = @s {ns}.zb.trap.id

# Candidates are the zombies in the box that the head can see; the nearest to the centre wins.
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag={ns}.zombie_round,tag=!{ns}.zb_rising,dx=$(sx),dy=$(sy),dz=$(sz)] run tag @s add {ns}._turret_cand
execute as @e[tag={ns}._turret_cand] run function {ns}:v{version}/zombies/traps/turret_check_los
# The tag's `store success` tells whether a target was picked (limit=1), with no extra @e scan.
scoreboard players set #turret_has_target {ns}.data 0
execute as @e[tag={ns}._turret_visible,sort=nearest,limit=1] store success score #turret_has_target {ns}.data run tag @s add {ns}._turret_target
tag @e[tag={ns}._turret_cand] remove {ns}._turret_cand
tag @e[tag={ns}._turret_visible] remove {ns}._turret_visible

execute if score #turret_has_target {ns}.data matches 0 run return 0

# Smoothed by teleport_duration.
execute as @e[tag={ns}.trap_head,predicate={ns}:v{version}/zombies/traps/turret_id_match] at @s run tp @s ~ ~ ~ facing entity @n[tag={ns}._turret_target] eyes

execute as @e[tag={ns}.trap_head,predicate={ns}:v{version}/zombies/traps/turret_id_match] at @s facing entity @n[tag={ns}._turret_target] eyes positioned ^ ^ ^1 run function {ns}:v{version}/zombies/traps/turret_shoot

tag @e[tag={ns}._turret_target] remove {ns}._turret_target
""")

	## The head sits half inside a barricade block and would block its own ray.
	## can_see_ata therefore casts from 1.5 below the interaction entity, matched by id.
	write_versioned_function("zombies/traps/turret_check_los", f"""
# Run as a candidate zombie.
scoreboard players set #turret_vis {ns}.data 0
execute at @e[tag={ns}.trap_interact,predicate={ns}:v{version}/zombies/traps/turret_id_match] positioned ~ ~-1.5 ~ store result score #turret_vis {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #turret_vis {ns}.data matches 1 run tag @s add {ns}._turret_visible
""")

	## piercing 0: the ray stops at the first entity.
	write_versioned_function("zombies/traps/turret_shoot", f"""
# Run as the trap centre, at the muzzle facing the target. G3A3 report and crack, as for a player.
particle minecraft:crit ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[distance=..64]
function {ns}:v{version}/sound/turret_fire

# A player between the turret and the zombies takes the bullet.
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

	## Run as the hit entity, at the hit point.
	write_versioned_function("zombies/traps/turret_hit", f"""
particle minecraft:crit ~ ~1 ~ 0.2 0.3 0.2 0.1 8 force @a[distance=..48]

# 45% of the zombie's max health.
execute if entity @s[tag={ns}.zombie_round] store result storage {ns}:temp _trap_dmg.amount int 1 run attribute @s minecraft:max_health get 0.45
execute if entity @s[tag={ns}.zombie_round] run data modify storage {ns}:temp _trap_dmg.type set value "{ns}:bullet"
execute if entity @s[tag={ns}.zombie_round] run return run function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _trap_dmg

execute if entity @s[type=player,gamemode=!creative,gamemode=!spectator] if score @s {ns}.zb.in_game matches 1.. run damage @s 2 {ns}:bullet
""")

