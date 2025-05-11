data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:20,display:{Name:"{\"text\":\"30-round 7.62×39mm\",\"italic\":false}",Lore:["{\"text\":\"AK47 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = ak47_mag S
function mgs:guns/_common/gen/mag
return 1