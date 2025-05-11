data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:210,Id:210,display:{Name:"{\"text\":\"MP5A3\",\"italic\":false}"}}
scoreboard players operation v0 V = mp5_damage S
scoreboard players operation v1 V = mp5_cooldown S
scoreboard players operation v2 V = mp5_acc_sneaky S
scoreboard players operation v3 V = mp5_mag S
scoreboard players operation v4 V = mp5_reload S
function mgs:guns/_common/gen/gun