data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:120,Id:120,display:{Name:"{\"text\":\"M9\",\"italic\":false}"}}
scoreboard players operation v0 V = m9_damage S
scoreboard players set v1 V 2
scoreboard players operation v2 V = m9_acc_sneaky S
scoreboard players operation v3 V = m9_mag S
scoreboard players operation v4 V = m9_reload S
function mgs:guns/_common/gen/gun