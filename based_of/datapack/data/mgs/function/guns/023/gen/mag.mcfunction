data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:230,display:{Name:"{\"text\":\"40-round HK 4.6x30mm\",\"italic\":false}",Lore:["{\"text\":\"MP7A1 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = mp7_mag S
function mgs:guns/_common/gen/mag
return 1