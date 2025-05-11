data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:170,display:{Name:"{\"text\":\"20-round .32 ACP\",\"italic\":false}",Lore:["{\"text\":\"Sa vz. 61 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = vz61_mag S
function mgs:guns/_common/gen/mag
return 1