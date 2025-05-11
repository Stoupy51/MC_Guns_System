data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:410,display:{Name:"{\"text\":\"10-round 7.62×54mmR\",\"italic\":false}",Lore:["{\"text\":\"SVD-63 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = svd_mag S
function mgs:guns/_common/gen/mag
return 1