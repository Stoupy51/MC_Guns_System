execute if score enableCatalogOnLoad V matches 1 run clear @a[tag=logged] minecraft:written_book{CustomModelData:1}
execute if score enableCatalogOnLoad V matches 1 as @a[tag=logged] at @s run function mgs_catalog:catalog
execute if score enableManualOnLoad V matches 1 run clear @a[tag=logged] minecraft:written_book{CustomModelData:2}
execute if score enableManualOnLoad V matches 1 as @a[tag=logged] at @s run function mgs_catalog:manual