
#> mgs:v5.0.0/utils/random_weapon
#
# @within	mgs:v5.0.0/mob/default/on_new {slot:"weapon.mainhand"}
#
# @args		slot (string)
#

execute store result score #random mgs.data run random value 1..31
$execute if score #random mgs.data matches 1 run loot replace entity @s $(slot) loot mgs:i/m16a4
$execute if score #random mgs.data matches 2 run loot replace entity @s $(slot) loot mgs:i/m16a4
$execute if score #random mgs.data matches 3 run loot replace entity @s $(slot) loot mgs:i/ak47
$execute if score #random mgs.data matches 4 run loot replace entity @s $(slot) loot mgs:i/fnfal
$execute if score #random mgs.data matches 5 run loot replace entity @s $(slot) loot mgs:i/aug
$execute if score #random mgs.data matches 6 run loot replace entity @s $(slot) loot mgs:i/m4a1
$execute if score #random mgs.data matches 7 run loot replace entity @s $(slot) loot mgs:i/g3a3
$execute if score #random mgs.data matches 8 run loot replace entity @s $(slot) loot mgs:i/famas
$execute if score #random mgs.data matches 9 run loot replace entity @s $(slot) loot mgs:i/scar17
$execute if score #random mgs.data matches 10 run loot replace entity @s $(slot) loot mgs:i/m1911
$execute if score #random mgs.data matches 11 run loot replace entity @s $(slot) loot mgs:i/m9
$execute if score #random mgs.data matches 12 run loot replace entity @s $(slot) loot mgs:i/deagle
$execute if score #random mgs.data matches 13 run loot replace entity @s $(slot) loot mgs:i/makarov
$execute if score #random mgs.data matches 14 run loot replace entity @s $(slot) loot mgs:i/glock17
$execute if score #random mgs.data matches 15 run loot replace entity @s $(slot) loot mgs:i/glock18
$execute if score #random mgs.data matches 16 run loot replace entity @s $(slot) loot mgs:i/vz61
$execute if score #random mgs.data matches 17 run loot replace entity @s $(slot) loot mgs:i/mp5
$execute if score #random mgs.data matches 18 run loot replace entity @s $(slot) loot mgs:i/mac10
$execute if score #random mgs.data matches 19 run loot replace entity @s $(slot) loot mgs:i/mp7
$execute if score #random mgs.data matches 20 run loot replace entity @s $(slot) loot mgs:i/ppsh41
$execute if score #random mgs.data matches 21 run loot replace entity @s $(slot) loot mgs:i/sten
$execute if score #random mgs.data matches 22 run loot replace entity @s $(slot) loot mgs:i/spas12
$execute if score #random mgs.data matches 23 run loot replace entity @s $(slot) loot mgs:i/m500
$execute if score #random mgs.data matches 24 run loot replace entity @s $(slot) loot mgs:i/m590
$execute if score #random mgs.data matches 25 run loot replace entity @s $(slot) loot mgs:i/svd
$execute if score #random mgs.data matches 26 run loot replace entity @s $(slot) loot mgs:i/m82
$execute if score #random mgs.data matches 27 run loot replace entity @s $(slot) loot mgs:i/mosin
$execute if score #random mgs.data matches 28 run loot replace entity @s $(slot) loot mgs:i/m24
$execute if score #random mgs.data matches 29 run loot replace entity @s $(slot) loot mgs:i/rpg7
$execute if score #random mgs.data matches 30 run loot replace entity @s $(slot) loot mgs:i/rpk
$execute if score #random mgs.data matches 31 run loot replace entity @s $(slot) loot mgs:i/m249

