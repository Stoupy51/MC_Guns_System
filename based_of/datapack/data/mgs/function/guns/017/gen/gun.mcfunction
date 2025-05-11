data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:170,Id:170,display:{Name:"{\"text\":\"Sa vz. 61\",\"italic\":false}"}}
scoreboard players operation v0 V = vz61_damage S
scoreboard players operation v1 V = vz61_cooldown S
scoreboard players operation v2 V = vz61_acc_sneaky S
scoreboard players operation v3 V = vz61_mag S
scoreboard players operation v4 V = vz61_reload S
function mgs:guns/_common/gen/gun