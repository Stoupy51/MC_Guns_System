data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:240,display:{Name:"{\"text\":\"71-round 7.62×25mm Tokarev\",\"italic\":false}",Lore:["{\"text\":\"PPSh-41 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = ppsh41_mag S
function mgs:guns/_common/gen/mag
return 1