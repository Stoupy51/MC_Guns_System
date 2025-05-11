data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:110,Id:110,display:{Name:"{\"text\":\"M1911A1\",\"italic\":false}"}}
scoreboard players operation v0 V = m1911_damage S
scoreboard players set v1 V 2
scoreboard players operation v2 V = m1911_acc_sneaky S
scoreboard players operation v3 V = m1911_mag S
scoreboard players operation v4 V = m1911_reload S
function mgs:guns/_common/gen/gun