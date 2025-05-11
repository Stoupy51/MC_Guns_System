data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:80,display:{Name:"{\"text\":\"20-round 7.62×51mm NATO\",\"italic\":false}",Lore:["{\"text\":\"FN MK 17 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = scar17_mag S
function mgs:guns/_common/gen/mag
return 1