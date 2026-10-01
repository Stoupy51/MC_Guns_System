
#> mgs:v5.1.0/grenade/move_semtex
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/tick
#

execute store result score #proj_gravity mgs.data run data get entity @s data.config.proj_gravity
scoreboard players operation @s bs.vel.y -= #proj_gravity mgs.data

# Sticks to the first surface or entity; during the launch grace period entities are skipped, so it never sticks to the thrower.
scoreboard players remove @s mgs.grenade_launch 1
execute if score @s mgs.grenade_launch matches 0.. run function #bs.move:apply_vel {scale:0.001,with:{blocks:true,entities:false,ignored_blocks:"#mgs:v5.1.0/projectile_pass_through",on_collision:"function mgs:v5.1.0/grenade/on_stick"}}
execute unless score @s mgs.grenade_launch matches 0.. run function #bs.move:apply_vel {scale:0.001,with:{blocks:true,entities:true,ignored_blocks:"#mgs:v5.1.0/projectile_pass_through",on_collision:"function mgs:v5.1.0/grenade/on_stick"}}

# white_smoke, which the shader marker detection does not mistake for a marker.
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

scoreboard players operation @s mgs.data -= #tick_delta mgs.data

execute if score @s mgs.data matches ..0 run function mgs:v5.1.0/grenade/detonate

