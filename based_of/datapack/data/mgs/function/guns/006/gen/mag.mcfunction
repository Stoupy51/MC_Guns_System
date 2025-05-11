data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:60,display:{Name:"{\"text\":\"20-round 7.62×51mm NATO\",\"italic\":false}",Lore:["{\"text\":\"G3A3 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = g3_mag S
function mgs:guns/_common/gen/mag
return 1