data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:60,Id:60,display:{Name:"{\"text\":\"G3A3\",\"italic\":false}"}}
scoreboard players operation v0 V = g3_damage S
scoreboard players operation v1 V = g3_cooldown S
scoreboard players operation v2 V = g3_acc_sneaky S
scoreboard players operation v3 V = g3_mag S
scoreboard players operation v4 V = g3_reload S
function mgs:guns/_common/gen/gun