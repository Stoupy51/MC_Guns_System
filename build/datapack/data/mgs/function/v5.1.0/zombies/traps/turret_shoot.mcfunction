
#> mgs:v5.1.0/zombies/traps/turret_shoot
#
# @executed	as @e[tag=mgs.trap_head,predicate=mgs:v5.1.0/zombies/traps/turret_id_match] & at @s & facing entity @n[tag=mgs._turret_target] eyes & positioned ^ ^ ^1
#
# @within	mgs:v5.1.0/zombies/traps/turret_fire [ as @e[tag=mgs.trap_head,predicate=mgs:v5.1.0/zombies/traps/turret_id_match] & at @s & facing entity @n[tag=mgs._turret_target] eyes & positioned ^ ^ ^1 ]
#

# Run as the trap centre, at the muzzle facing the target. G3A3 report and crack, as for a player.
particle minecraft:crit ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[distance=..64]
function mgs:v5.1.0/sound/turret_fire

# A player between the turret and the zombies takes the bullet.
data modify storage mgs:input with set value {}
data modify storage mgs:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage mgs:input with.entities set value "!global.ignore"
data modify storage mgs:input with.piercing set value 0
data modify storage mgs:input with.max_distance set value 32
data modify storage mgs:input with.ignored_blocks set value "#mgs:v5.1.0/empty"
data modify storage mgs:input with.ignored_entities set value "#mgs:ignore"
data modify storage mgs:input with.on_targeted_entity set value "function mgs:v5.1.0/zombies/traps/turret_hit"
function #bs.raycast:run with storage mgs:input

