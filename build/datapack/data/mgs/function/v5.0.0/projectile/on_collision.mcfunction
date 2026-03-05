
#> mgs:v5.0.0/projectile/on_collision
#
# @within	???
#

# Tag the nearest non-immune entity as directly hit (for bullet damage in explode)
# distance=..2.5 covers feet-to-head hit at any entity height up to 2.5 blocks
execute as @n[distance=..2.5,type=!#bs.hitbox:intangible,tag=!mgs.slow_bullet] run tag @s add mgs.direct_hit

# Mark for explosion
tag @s add mgs.exploding

# Stop all remaining velocity to prevent further movement
scoreboard players set $move.vel.x bs.lambda 0
scoreboard players set $move.vel.y bs.lambda 0
scoreboard players set $move.vel.z bs.lambda 0

