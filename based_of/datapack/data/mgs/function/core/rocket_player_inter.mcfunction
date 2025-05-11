execute if block ~ ~ ~ #mgs:sounds/glass run playsound minecraft:block.glass.break block @a ~ ~ ~ 1
execute if block ~ ~ ~ #mgs:sounds/water run playsound minecraft:ambient.underwater.exit block @a ~ ~ ~ 0.25 1.5
execute positioned ~ ~-1.7 ~ as @a[distance=0..1.5,tag=!dead,tag=!own] run playsound mgs:common.rocket_fly_by block @s ~ ~ ~ 1
execute positioned ~ ~-0.975 ~ positioned ^ ^ ^0.5 as @e[type=minecraft:marker,tag=lp,distance=0..1.14,tag=!hit,tag=!own] if score @s timestamp = time V run function mgs:util/hitbox_p