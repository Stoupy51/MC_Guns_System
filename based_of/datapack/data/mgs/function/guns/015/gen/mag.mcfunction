data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:150,display:{Name:"{\"text\":\"17-round 9×19mm Parabellum\",\"italic\":false}",Lore:["{\"text\":\"Glock 17 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = glock17_mag S
function mgs:guns/_common/gen/mag
return 1