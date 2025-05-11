data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:150,Id:150,display:{Name:"{\"text\":\"Glock 17\",\"italic\":false}"}}
scoreboard players operation v0 V = glock17_damage S
scoreboard players set v1 V 2
scoreboard players operation v2 V = glock17_acc_sneaky S
scoreboard players operation v3 V = glock17_mag S
scoreboard players operation v4 V = glock17_reload S
function mgs:guns/_common/gen/gun