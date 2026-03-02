
#> mgs:v5.0.0/grenade/on_stick
#
# @within	???
#

# Stop all velocity (stick to the surface)
function #bs.move:callback/stick

# Mark as stuck so tick skips movement
tag @s add mgs.grenade_stuck

# If we hit an entity (hit_flag = -1 for entities), pair the grenade with the target
execute if score $move.hit_flag bs.lambda matches -1 run function mgs:v5.0.0/grenade/stick_to_entity

# Play stick sound
playsound minecraft:block.honey_block.place player @a[distance=..32] ~ ~ ~ 1 1.2

