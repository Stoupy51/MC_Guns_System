data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:130,display:{Name:"{\"text\":\"7-round .50 AE\",\"italic\":false}",Lore:["{\"text\":\"Desert Eagle Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = deagle_mag S
function mgs:guns/_common/gen/mag
return 1