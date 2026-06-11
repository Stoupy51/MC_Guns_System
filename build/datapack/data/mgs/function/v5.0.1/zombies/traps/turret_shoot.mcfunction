
#> mgs:v5.0.1/zombies/traps/turret_shoot
#
# @executed	as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] & at @s
#
# @within	mgs:v5.0.1/zombies/traps/turret_fire
#

# @s = target zombie (execution position = turret head, facing the target)
# Tracer particle + shot sound
particle minecraft:crit ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[distance=..64]
playsound minecraft:entity.arrow.shoot block @a[distance=..32] ~ ~ ~ 0.8 1.6

# Raycast with piercing 0: the ray stops at the first entity hit,
# so a player standing between the turret and the zombies takes the bullet instead
data modify storage mgs:input with set value {}
data modify storage mgs:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage mgs:input with.entities set value true
data modify storage mgs:input with.piercing set value 0
data modify storage mgs:input with.max_distance set value 32
data modify storage mgs:input with.ignored_blocks set value "#mgs:v5.0.1/empty"
data modify storage mgs:input with.ignored_entities set value "#mgs:ignore"
data modify storage mgs:input with.on_targeted_entity set value "function mgs:v5.0.1/zombies/traps/turret_hit"
function #bs.raycast:run with storage mgs:input

