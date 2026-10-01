
#> mgs:v5.1.0/projectile/on_collision
#
# @executed	at @s
#
# @within	mgs:v5.1.0/projectile/tick {scale:0.001,with:{blocks:true,entities:true,ignored_blocks:"#mgs:v5.1.0/projectile_pass_through",on_collision:"function mgs:v5.1.0/projectile/on_collision"}}
#

# The nearest non-immune entity takes the direct-hit damage in explode; 2.5 blocks covers feet to head at any height up to 2.5.
tag @e[tag=mgs.direct_hit] remove mgs.direct_hit
execute as @n[distance=..2.5,type=!#mgs:ignore,tag=!mgs.slow_bullet,tag=!global.ignore.kill,tag=!global.ignore,nbt=!{Invulnerable:true}] run tag @s add mgs.direct_hit

tag @s add mgs.exploding

scoreboard players set $move.vel.x bs.lambda 0
scoreboard players set $move.vel.y bs.lambda 0
scoreboard players set $move.vel.z bs.lambda 0

