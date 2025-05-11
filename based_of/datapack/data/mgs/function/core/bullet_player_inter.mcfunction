execute if score enableTracer V matches 1 run particle minecraft:mycelium ~ ~ ~ 0 0 0 0 1
execute if score v15 V matches 2.. run function mgs:core/bullet_collide
execute positioned ~ ~-1.7 ~ as @a[distance=0..1.5,tag=!dead,tag=!own] run playsound mgs:common.bullet_fly_by block @s ~ ~ ~ 1
execute positioned ~ ~-0.975 ~ positioned ^ ^ ^0.5 as @e[type=minecraft:marker,tag=lp,distance=0..1.14,tag=!hit,tag=!own] if score @s timestamp = time V run function mgs:util/hitbox_p