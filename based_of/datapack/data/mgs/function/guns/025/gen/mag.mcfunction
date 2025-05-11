data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:250,display:{Name:"{\"text\":\"32-round 9×19mm Parabellum\",\"italic\":false}",Lore:["{\"text\":\"Sten MK II Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = sten_mag S
function mgs:guns/_common/gen/mag
return 1