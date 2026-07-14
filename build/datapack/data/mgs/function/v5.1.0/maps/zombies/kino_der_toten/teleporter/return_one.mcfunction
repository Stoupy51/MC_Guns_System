
#> mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/return_one
#
# @executed	as @a[tag=mgs.kino.in_tp]
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/return_players [ as @a[tag=mgs.kino.in_tp] ]
#

# @s = player returning from theater — pick a random lobby spot
execute store result score #tp_random mgs.data run random value 1..5
execute if score #tp_random mgs.data matches 1 run tp @s ~9 ~-4 ~-40
execute if score #tp_random mgs.data matches 2 run tp @s ~-34 ~4 ~54
execute if score #tp_random mgs.data matches 3 run tp @s ~-27 ~4 ~-82
execute if score #tp_random mgs.data matches 4 run tp @s ~-97 ~7 ~13
execute if score #tp_random mgs.data matches 5 run tp @s ~40 ~4 ~39
execute at @s run playsound minecraft:entity.enderman.teleport block @s ~ ~ ~ 1 1

