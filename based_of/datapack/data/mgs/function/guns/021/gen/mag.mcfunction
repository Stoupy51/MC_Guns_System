data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:210,display:{Name:"{\"text\":\"30-round 9×19mm Parabellum\",\"italic\":false}",Lore:["{\"text\":\"MP5A3 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = mp5_mag S
function mgs:guns/_common/gen/mag
return 1