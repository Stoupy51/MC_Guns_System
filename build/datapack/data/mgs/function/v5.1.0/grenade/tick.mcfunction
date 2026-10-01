
#> mgs:v5.1.0/grenade/tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/tick [ at @s ]
#

# Stuck (semtex on a surface) or in its smoke or flash phase.
execute if entity @s[tag=mgs.grenade_stuck] run return run function mgs:v5.1.0/grenade/tick_stuck
execute if entity @s[tag=mgs.grenade_active_effect] run return run function mgs:v5.1.0/grenade/tick_effect

# Tumble in proportion to speed, so it stops spinning as it comes to rest.
# #gr_speed = |vx| + |vy| + |vz|, in thousandths of a block per tick.
scoreboard players operation #gr_speed mgs.data = @s bs.vel.x
execute if score #gr_speed mgs.data matches ..-1 run scoreboard players operation #gr_speed mgs.data *= #minus_one mgs.data
scoreboard players operation #gr_sv mgs.data = @s bs.vel.y
execute if score #gr_sv mgs.data matches ..-1 run scoreboard players operation #gr_sv mgs.data *= #minus_one mgs.data
scoreboard players operation #gr_speed mgs.data += #gr_sv mgs.data
scoreboard players operation #gr_sv mgs.data = @s bs.vel.z
execute if score #gr_sv mgs.data matches ..-1 run scoreboard players operation #gr_sv mgs.data *= #minus_one mgs.data
scoreboard players operation #gr_speed mgs.data += #gr_sv mgs.data

# About 0.44 rad per block/tick of speed, in 1e-4 rad units; no update at rest.
scoreboard players operation #gr_speed mgs.data *= #44 mgs.data
scoreboard players operation #gr_speed mgs.data /= #10 mgs.data
execute if score #gr_speed mgs.data matches 1.. run function mgs:v5.1.0/grenade/spin_tick

execute store result score #proj_gravity mgs.data run data get entity @s data.config.proj_gravity
scoreboard players operation @s bs.vel.y -= #proj_gravity mgs.data

# Bookshelf move with collision: damped_bounce (frag, smoke, flash) or stick (semtex, web).
execute if data entity @s data.config{grenade_type:"semtex"} run return run function mgs:v5.1.0/grenade/move_semtex
execute if data entity @s data.config{grenade_type:"web"} run return run function mgs:v5.1.0/grenade/move_semtex
function #bs.move:apply_vel {scale:0.001,with:{blocks:true,entities:false,ignored_blocks:"#mgs:v5.1.0/projectile_pass_through",on_collision:"function mgs:v5.1.0/grenade/on_bounce"}}

# white_smoke, which the shader marker detection does not mistake for a marker.
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

# Attraction (taunt and aggro pulses); does nothing outside zombies.
execute if entity @s[tag=mgs.monkey_bomb] at @s run function mgs:v5.1.0/zombies/monkey/tick

scoreboard players operation @s mgs.data -= #tick_delta mgs.data

execute if score @s mgs.data matches ..0 run function mgs:v5.1.0/grenade/detonate

