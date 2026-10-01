
#> mgs:v5.1.0/grenade/on_bounce
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/tick {scale:0.001,with:{blocks:true,entities:false,ignored_blocks:"#mgs:v5.1.0/projectile_pass_through",on_collision:"function mgs:v5.1.0/grenade/on_bounce"}}
#

function #bs.move:callback/damped_bounce

playsound minecraft:entity.item.pickup player @a[distance=..32] ~ ~ ~ 0.5 0.5

