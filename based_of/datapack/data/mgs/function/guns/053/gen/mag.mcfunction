data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:530,display:{Name:"{\"text\":\"150-round 5.56×45mm NATO\",\"italic\":false}",Lore:["{\"text\":\"M249 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = m249_mag S
function mgs:guns/_common/gen/mag
return 1