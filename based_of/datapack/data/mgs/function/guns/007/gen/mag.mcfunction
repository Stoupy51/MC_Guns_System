data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:70,display:{Name:"{\"text\":\"25-round 5.56×45mm NATO\",\"italic\":false}",Lore:["{\"text\":\"FAMAS F1 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = famas_mag S
function mgs:guns/_common/gen/mag
return 1