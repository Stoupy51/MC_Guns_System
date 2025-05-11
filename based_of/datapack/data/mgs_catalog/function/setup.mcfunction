# Must be loaded after MGS!!!
execute unless score enableCatalogOnLoad V matches 0.. run scoreboard players set enableCatalogOnLoad V 1
execute unless score enableManualOnLoad V matches 0.. run scoreboard players set enableManualOnLoad V 1
scoreboard objectives add catalog_last dummy