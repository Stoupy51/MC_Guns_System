data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:230,Id:230,display:{Name:"{\"text\":\"MP7A1\",\"italic\":false}"}}
scoreboard players operation v0 V = mp7_damage S
scoreboard players operation v1 V = mp7_cooldown S
scoreboard players operation v2 V = mp7_acc_sneaky S
scoreboard players operation v3 V = mp7_mag S
scoreboard players operation v4 V = mp7_reload S
function mgs:guns/_common/gen/gun