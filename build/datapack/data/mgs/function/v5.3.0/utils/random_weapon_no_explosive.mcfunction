
#> mgs:v5.3.0/utils/random_weapon_no_explosive
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/mob/arm
#

execute store result score #random mgs.data run random value 1..29
execute if score #random mgs.data matches 1 run return run loot replace entity @s weapon.mainhand loot mgs:i/ak47
execute if score #random mgs.data matches 2 run return run loot replace entity @s weapon.mainhand loot mgs:i/m16a4
execute if score #random mgs.data matches 3 run return run loot replace entity @s weapon.mainhand loot mgs:i/famas
execute if score #random mgs.data matches 4 run return run loot replace entity @s weapon.mainhand loot mgs:i/aug
execute if score #random mgs.data matches 5 run return run loot replace entity @s weapon.mainhand loot mgs:i/m4a1
execute if score #random mgs.data matches 6 run return run loot replace entity @s weapon.mainhand loot mgs:i/fnfal
execute if score #random mgs.data matches 7 run return run loot replace entity @s weapon.mainhand loot mgs:i/g3a3
execute if score #random mgs.data matches 8 run return run loot replace entity @s weapon.mainhand loot mgs:i/scar17
execute if score #random mgs.data matches 9 run return run loot replace entity @s weapon.mainhand loot mgs:i/mp5
execute if score #random mgs.data matches 10 run return run loot replace entity @s weapon.mainhand loot mgs:i/mp7
execute if score #random mgs.data matches 11 run return run loot replace entity @s weapon.mainhand loot mgs:i/mac10
execute if score #random mgs.data matches 12 run return run loot replace entity @s weapon.mainhand loot mgs:i/ppsh41
execute if score #random mgs.data matches 13 run return run loot replace entity @s weapon.mainhand loot mgs:i/sten
execute if score #random mgs.data matches 14 run return run loot replace entity @s weapon.mainhand loot mgs:i/m249
execute if score #random mgs.data matches 15 run return run loot replace entity @s weapon.mainhand loot mgs:i/rpk
execute if score #random mgs.data matches 16 run return run loot replace entity @s weapon.mainhand loot mgs:i/svd
execute if score #random mgs.data matches 17 run return run loot replace entity @s weapon.mainhand loot mgs:i/m82
execute if score #random mgs.data matches 18 run return run loot replace entity @s weapon.mainhand loot mgs:i/mosin
execute if score #random mgs.data matches 19 run return run loot replace entity @s weapon.mainhand loot mgs:i/m24
execute if score #random mgs.data matches 20 run return run loot replace entity @s weapon.mainhand loot mgs:i/spas12
execute if score #random mgs.data matches 21 run return run loot replace entity @s weapon.mainhand loot mgs:i/m500
execute if score #random mgs.data matches 22 run return run loot replace entity @s weapon.mainhand loot mgs:i/m590
execute if score #random mgs.data matches 23 run return run loot replace entity @s weapon.mainhand loot mgs:i/m1911
execute if score #random mgs.data matches 24 run return run loot replace entity @s weapon.mainhand loot mgs:i/m9
execute if score #random mgs.data matches 25 run return run loot replace entity @s weapon.mainhand loot mgs:i/deagle
execute if score #random mgs.data matches 26 run return run loot replace entity @s weapon.mainhand loot mgs:i/makarov
execute if score #random mgs.data matches 27 run return run loot replace entity @s weapon.mainhand loot mgs:i/glock17
execute if score #random mgs.data matches 28 run return run loot replace entity @s weapon.mainhand loot mgs:i/glock18
execute if score #random mgs.data matches 29 run return run loot replace entity @s weapon.mainhand loot mgs:i/vz61

