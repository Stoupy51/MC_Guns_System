data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:160,display:{Name:"{\"text\":\"19-round 9×19mm Parabellum\",\"italic\":false}",Lore:["{\"text\":\"Glock 18 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = glock18_mag S
function mgs:guns/_common/gen/mag
return 1