
#> mgs:v5.0.0/projectile/on_collision
#
# @within	???
#

# Mark for explosion
tag @s add mgs.exploding

# Stop all remaining velocity to prevent further movement
scoreboard players set $move.vel.x bs.lambda 0
scoreboard players set $move.vel.y bs.lambda 0
scoreboard players set $move.vel.z bs.lambda 0

