data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:160,Id:160,display:{Name:"{\"text\":\"Glock 18\",\"italic\":false}"}}
scoreboard players operation v0 V = glock18_damage S
scoreboard players operation v1 V = glock18_cooldown S
scoreboard players operation v2 V = glock18_acc_sneaky S
scoreboard players operation v3 V = glock18_mag S
scoreboard players operation v4 V = glock18_reload S
function mgs:guns/_common/gen/gun