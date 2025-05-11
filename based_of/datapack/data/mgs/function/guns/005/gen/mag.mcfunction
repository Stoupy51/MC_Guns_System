data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:50,display:{Name:"{\"text\":\"30-round 5.56×45mm NATO\",\"italic\":false}",Lore:["{\"text\":\"M4A1 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = m4_mag S
function mgs:guns/_common/gen/mag
return 1