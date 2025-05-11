data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:140,Id:140,display:{Name:"{\"text\":\"PM\",\"italic\":false}"}}
scoreboard players operation v0 V = makarov_damage S
scoreboard players set v1 V 2
scoreboard players operation v2 V = makarov_acc_sneaky S
scoreboard players operation v3 V = makarov_mag S
scoreboard players operation v4 V = makarov_reload S
function mgs:guns/_common/gen/gun