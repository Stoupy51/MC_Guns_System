#v0 10 * t, v1 1000*dx, v2 1000*dy, v3 1000*dz, v4 1000*x, v5 1000*y, v6 1000*z, v13 running_t
scoreboard players set v14 V -1

execute positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^-0.05 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V -2
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.00 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 0
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.05 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 1
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.10 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 1
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.15 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 2
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.20 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 2
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.25 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 3
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.30 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 3
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.35 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 4
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.40 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 4
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.45 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 5
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.50 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 5
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.55 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 6
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.60 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 6
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.65 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 7
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.70 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 7
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.75 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 8
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.80 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 8
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.85 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 9
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.90 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 9
execute if score v14 V matches -1 positioned ~-0.015 ~-0.015 ~-0.015 positioned ^ ^ ^0.95 if entity @s[tag=!hit,dx=0] positioned ~-0.97 ~-0.97 ~-0.97 if entity @s[dx=0] run scoreboard players set v14 V 10

#auxilliary commands:
execute if score v14 V <= v13 V if score v14 V matches 0.. run tag @s add hit
execute if entity @s[tag=hit] run scoreboard players add @p[tag=own] mobhits 1
execute as @s[tag=hit] run function mgs:util/damage_reg