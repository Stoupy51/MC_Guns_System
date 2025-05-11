data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:120,display:{Name:"{\"text\":\"15-round 9×19mm Parabellum\",\"italic\":false}",Lore:["{\"text\":\"M9 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = m9_mag S
function mgs:guns/_common/gen/mag
return 1