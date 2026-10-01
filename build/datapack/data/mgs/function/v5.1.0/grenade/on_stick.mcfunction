
#> mgs:v5.1.0/grenade/on_stick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/move_semtex {scale:0.001,with:{blocks:true,entities:false,ignored_blocks:"#mgs:v5.1.0/projectile_pass_through",on_collision:"function mgs:v5.1.0/grenade/on_stick"}}
#			mgs:v5.1.0/grenade/move_semtex {scale:0.001,with:{blocks:true,entities:true,ignored_blocks:"#mgs:v5.1.0/projectile_pass_through",on_collision:"function mgs:v5.1.0/grenade/on_stick"}}
#

function #bs.move:callback/stick

# The tick skips movement.
tag @s add mgs.grenade_stuck

# hit_flag -1 is an entity: pair the grenade with it.
execute if score $move.hit_flag bs.lambda matches -1 run function mgs:v5.1.0/grenade/stick_to_entity

# A web grenade bursts at once on a mob hit, but waits its fuse on a surface.
execute if score $move.hit_flag bs.lambda matches -1 if data entity @s data.config{grenade_type:"web"} run return run function mgs:v5.1.0/grenade/detonate

playsound minecraft:block.honey_block.place player @a[distance=..32] ~ ~ ~ 1 1.2

