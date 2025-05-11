data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:140,display:{Name:"{\"text\":\"8-round 9×18mm PM\",\"italic\":false}",Lore:["{\"text\":\"PM Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = makarov_mag S
function mgs:guns/_common/gen/mag
return 1