data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:420,display:{Name:"{\"text\":\"10-round .50 BMG\",\"italic\":false}",Lore:["{\"text\":\"M82A1 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = m82_mag S
function mgs:guns/_common/gen/mag
return 1