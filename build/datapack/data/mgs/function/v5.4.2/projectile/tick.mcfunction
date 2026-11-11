
#> mgs:v5.4.2/projectile/tick
#
# @executed	at @s
#
# @within	mgs:v5.4.2/tick [ at @s ]
#			mgs:v5.4.2/dialog/close_then
#

execute store result score #proj_gravity mgs.data run data get entity @s data.config.proj_gravity
scoreboard players operation @s bs.vel.y -= #proj_gravity mgs.data

# Bookshelf move with collision; custom ignored_blocks, so barriers never stop projectiles.
function #bs.move:apply_vel {scale:0.001,with:{blocks:true,entities:true,ignored_blocks:"#mgs:v5.4.2/projectile_pass_through",on_collision:"function mgs:v5.4.2/projectile/on_collision"}}

execute at @s run function mgs:v5.4.2/projectile/post_vel

