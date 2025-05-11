data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:220,display:{Name:"{\"text\":\"30-round .45 ACP\",\"italic\":false}",Lore:["{\"text\":\"MAC-10 Ammunition\",\"italic\":false,\"color\":\"gray\"}"]}}
scoreboard players operation v1 V = mac10_mag S
function mgs:guns/_common/gen/mag
return 1