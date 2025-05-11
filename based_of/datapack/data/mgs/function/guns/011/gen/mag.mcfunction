data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:110,display:{Name:"{\"text\":\"7-round .45 ACP\",\"italic\":false}",Lore:["{\"text\":\"M1911A1 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = m1911_mag S
function mgs:guns/_common/gen/mag
return 1