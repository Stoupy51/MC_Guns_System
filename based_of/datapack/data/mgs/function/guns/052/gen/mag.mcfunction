data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:520,display:{Name:"{\"text\":\"75-round 7.62×39mm\",\"italic\":false}",Lore:["{\"text\":\"RPK Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = rpk_mag S
function mgs:guns/_common/gen/mag
return 1